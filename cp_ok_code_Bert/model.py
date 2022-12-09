# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 21:06:25 2020

@author: zhaog
"""
import torch
from torch import nn
from transformers import BertForSequenceClassification, BertConfig


class BertModel(nn.Module):
    def __init__(self):
        super(BertModel, self).__init__()
        self.bert = BertForSequenceClassification.from_pretrained(
            "/home/xums/projects/python/cp_ok_code_Bert/models/bert_base_uncased", num_labels=2)  # /bert_pretrain/
        self.device = torch.device("cuda")
        for param in self.bert.parameters():
            param.requires_grad = True  # 每个参数都要 求梯度

    def forward(self, batch_seqs, batch_seq_masks, batch_seq_segments, labels):
        # loss, logits = self.bert(input_ids = batch_seqs, attention_mask = batch_seq_masks,
        #                      token_type_ids=batch_seq_segments, labels = labels)
        output = self.bert(input_ids=batch_seqs, attention_mask=batch_seq_masks,
                           token_type_ids=batch_seq_segments, labels=labels)
        # print(output)
        # print(type(output))
        loss = output[0]

        logits = output[1]

        probabilities = nn.functional.softmax(logits, dim=-1)
        return loss, logits, probabilities


class BertModelTest(nn.Module):
    def __init__(self):
        super(BertModelTest, self).__init__()
        config = BertConfig.from_pretrained(
            '/home/xums/projects/python/cp_ok_code_Bert/models/bert_base_uncased/config.json')
        self.bert = BertForSequenceClassification(config)  # /bert_pretrain/
        self.device = torch.device("cuda")

    def forward(self, batch_seqs, batch_seq_masks, batch_seq_segments, labels):
        loss, logits = self.bert(input_ids=batch_seqs, attention_mask=batch_seq_masks,
                                 token_type_ids=batch_seq_segments, labels=labels)
        probabilities = nn.functional.softmax(logits, dim=-1)
        return loss, logits, probabilities
