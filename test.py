from model import GPTModel
from trainer import GPTTrainer

model = GPTModel()
trainer = GPTTrainer('./dataset/squad.json', model)

trained_model = trainer.train()
trained_model.save('./first_model')
