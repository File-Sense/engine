import torch
import torch.nn as nn
import torchvision.models as models  # type: ignore


class Encoder(nn.Module):
    def __init__(self, embed_size):
        super(Encoder, self).__init__()
        resnet = models.resnet50(pretrained=True)

        for param in list(resnet.parameters())[:-6]:
            param.requires_grad_(False)
        for param in list(resnet.parameters())[-6:]:
            param.requires_grad_(True)

        modules = list(resnet.children())[:-1]
        self.resnet = nn.Sequential(*modules)
        self.embed = nn.Linear(resnet.fc.in_features, embed_size)
        self.batch_norm = nn.BatchNorm1d(embed_size, momentum=0.01)
        self.dropout = nn.Dropout(0.5)

    def forward(self, images):
        features = self.resnet(images)
        features = features.view(features.size(0), -1)
        features = self.embed(features)
        features = self.batch_norm(features)
        return features


class Decoder(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers=1, dropout=0.5):
        super(Decoder, self).__init__()
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.vocab_size = vocab_size
        self.num_layers = num_layers

        self.word_embedding = nn.Embedding(self.vocab_size, self.embed_size)
        self.lstm = nn.LSTM(
            self.embed_size,
            self.hidden_size,
            self.num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
        )

        self.layer_norm = nn.LayerNorm(self.hidden_size)
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(self.hidden_size, self.vocab_size)

    def forward(self, features, captions):
        caption_embed = self.word_embedding(captions[:, :-1])
        caption_embed = torch.cat((features.unsqueeze(dim=1), caption_embed), 1)
        output, _ = self.lstm(caption_embed)
        output = self.fc(output)
        return output

    def sample(self, inputs, states=None, max_len=20):
        output = []
        (h, c) = (
            torch.randn(self.num_layers, 1, self.hidden_size).to(inputs.device),
            torch.randn(self.num_layers, 1, self.hidden_size).to(inputs.device),
        )
        for i in range(max_len):
            x, (h, c) = self.lstm(inputs, (h, c))
            x = self.fc(x)
            x = x.squeeze(1)
            predict = x.argmax(dim=1)
            if predict.item() == 1:
                break
            output.append(predict.item())
            inputs = self.word_embedding(predict.unsqueeze(0))
        return output
