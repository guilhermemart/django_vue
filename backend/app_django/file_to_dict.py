# recebe um path para um txt ou csv e retorna um dict com os dados dele

def file_to_dict(file):
    try:
        with open(file, "r") as f:
            the_list = []
            for line in f:
                sp = line.split(",")
                name = sp[0].strip().split(" ")[1]
                sub_dict = {
                    "largura": int(sp[1].strip().split(" ")[1]),
                    "altura": int(sp[2].strip().split(" ")[1]),
                    "pontos": [float(sp[3].strip().split(" ")[1]), float(sp[4])]}
                i = 5
                while i < len(sp):
                    sub_dict["pontos"].extend([float(sp[i]), float(sp[i+1])])
                    i += 2
                # yield(dict)
                the_list.append({name: sub_dict})
        f.close()
    except Exception as e:
        print(e)
        the_list = [{"name": "file not found"}]
    return the_list


if __name__ == '__main__':
    file_name = "cam1"
    the_dict = file_to_dict(file_name)
    print(the_dict)