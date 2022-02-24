# Usado no 'alerts_report', recebe uma lista de alertas e retorna um dict com os dados de resumo
def report_data(alerts):
    # Dados zerados para poder dar incremento
    report_data = {"total": 0, "nonconformity": 0, "redzone": 0, "approved": 0, "disapproved": 0, "unclassified": 0}
    # Adiciona a quantidade ao total e categoria
    # Verifica se é aprovado, desaprovado ou não classificado
    for alert in alerts:
        report_data["total"] += alert["quantidade"]
        report_data[alert["get_category_name"].lower()] += alert["quantidade"]
        if alert["thumb_up"]:
            report_data["approved"] += 1
        elif alert["thumb_down"]:
            report_data["disapproved"] += 1
        else:
            report_data["unclassified"] += 1

    return report_data