from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO


class PDFService:

    @staticmethod
    def expense_receipt(expense, group, user, participants):

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=LETTER,
            leftMargin=40,
            rightMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        # Estilos personalizados
        title_style = ParagraphStyle(
            "TitleCustom",
            parent=styles["Title"],
            textColor=colors.HexColor("#333333"),
            fontSize=20,
            leading=24,
            alignment=1  # Centrado
        )

        card_style = ParagraphStyle(
            "Card",
            parent=styles["Normal"],
            backColor=colors.HexColor("#f7f7f7"),
            fontSize=11,
            leading=14,
            leftIndent=10,
            rightIndent=10,
            spaceAfter=10,
            borderPadding=8,
            borderRadius=6
        )

        elements = []

        # ----------------------
        # TÍTULO
        # ----------------------
        elements.append(Paragraph("Factura de Gasto - DiviPay", title_style))
        elements.append(Spacer(1, 16))

        # ----------------------
        # ENCABEZADO (estilo tarjeta)
        # ----------------------
        header_text = f"""
            <b>Grupo:</b> {group.name}<br/>
            <b>Registrado por:</b> {user.name}<br/>
            <b>Fecha:</b> {expense.created_at.strftime('%Y-%m-%d %H:%M')}
        """
        elements.append(Paragraph(header_text, card_style))
        elements.append(Spacer(1, 10))

        # ----------------------
        # INFORMACIÓN DEL GASTO
        # ----------------------
        elements.append(Paragraph("<b>Detalle del gasto</b>", styles["Heading3"]))

        data_gasto = [
            ["Título:", expense.title],
            ["Monto total:", f"${expense.amount:,.0f}"],
            ["Categoría:", expense.category or "Sin categoría"]
        ]

        gasto_table = Table(
            data_gasto,
            colWidths=[120, 330]
        )

        gasto_table.setStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#444444")),
            ("TEXTCOLOR", (1, 0), (1, -1), colors.black),
            ("ALIGN", (0, 0), (0, -1), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])

        elements.append(gasto_table)
        elements.append(Spacer(1, 18))

        # ----------------------
        # TABLA DE PARTICIPANTES
        # ----------------------
        elements.append(Paragraph("<b>Aportes individuales</b>", styles["Heading3"]))

        table_data = [["Participante", "Aporte"]]

        for p in participants:
            table_data.append([p["name"], f"${p['contribution']:,.0f}"])

        table = Table(table_data, colWidths=[300, 150])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e2e2")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 25))

        # ----------------------
        # CIERRE
        # ----------------------
        elements.append(Paragraph(
            "<font size=10 color='#555555'>Gracias por usar DiviPay 💙</font>",
            styles["Normal"]
        ))

        # Construcción del PDF
        doc.build(elements)

        buffer.seek(0)
        return buffer
