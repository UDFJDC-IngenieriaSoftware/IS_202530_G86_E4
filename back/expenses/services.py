#Lógica de división de pagos


def calculate_split(expense_data):
    total = expense_data.amount_total
    participants = expense_data.participants
    n = len(participants)

    #Division equitativa
    if expense_data.split_method == "equal":
        per_person = round(total / n, 2)
        for p in participants:
            p.amount_owed = per_person
        return participants

    #Division por porcentaje
    if expense_data.split_method == "percentage":
        sum_perc = sum(p.percentage for p in participants)
        if sum_perc != 100:
            raise ValueError("Los porcentajes deben sumar 100%")
        for p in participants:
            p.amount_owed = round((p.percentage / 100) * total, 2)
        return participants

    #División manual
    if expense_data.split_method == "manual":
        total_manual = sum(p.amount_owed for p in participants)
        if round(total_manual, 2) != round(total, 2):
            raise ValueError("La suma de los montos no coincide con el total")
        return participants

    raise ValueError("Método de división inválido")
