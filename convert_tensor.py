import json
import torch

with open('input_code_final.json') as input_code_final:
    inputdata = json.load(input_code_final)

with open('output_tokenizer.json') as output_code_final:
    outputdata = json.load(output_code_final)


dict_input_code = {}
dict_input_seg = {}
for data in inputdata:
    hash_in, code, seg = data
    dict_input_code[hash_in] = code
    dict_input_seg[hash_in] = seg
dict_output = dict(outputdata)

tensor_in = []
tensor_out = []
for keys in dict_input_code.keys():
    input_tensor = [torch.tensor(dict_input_code[keys]),torch.tensor(dict_input_seg[keys])]
    output_tensor = torch.tensor(dict_output[keys])
    tensor_in.append(input_tensor)
    tensor_out.append(output_tensor)

torch.save(tensor_in,'input.pt')
torch.save(tensor_out,'output.pt')