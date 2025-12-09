from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import os


class PDFService:

    @staticmethod
    def expense_receipt(expense, group, user, participants):

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=LETTER,
            leftMargin=40,
            rightMargin=40,
            topMargin=30,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        elements = []

        # ----------------------
        # HEADER CON LOGO
        # ----------------------
        # Intentar cargar el logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "front", "logo.png")
        
        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=0.8*inch, height=0.8*inch)
                logo.hAlign = 'LEFT'
                elements.append(logo)
                elements.append(Spacer(1, 10))
            except:
                pass  # Si falla, continuar sin logo

        # Título principal con estilo moderno
        title_style = ParagraphStyle(
            "ModernTitle",
            parent=styles["Title"],
            textColor=colors.HexColor("#1a1a1a"),
            fontSize=24,
            fontName="Helvetica-Bold",
            leading=28,
            spaceAfter=8,
            alignment=0  # Izquierda
        )
        
        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            textColor=colors.HexColor("#666666"),
            fontSize=11,
            leading=14,
            spaceAfter=20
        )

        elements.append(Paragraph("Recibo de Gasto", title_style))
        elements.append(Paragraph(f"DiviPay • {expense.date.strftime('%d de %B, %Y')}", subtitle_style))
        
        # Línea divisoria moderna
        line_table = Table([[""]], colWidths=[7.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 3, colors.HexColor("#4F46E5")),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 20))

        # ----------------------
        # INFORMACIÓN DEL GRUPO (Card moderna)
        # ----------------------
        card_style = ParagraphStyle(
            "Card",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#374151")
        )

        group_info = f"""
            <para>
            <b><font size=11 color="#1f2937">Grupo:</font></b> {group.name}<br/>
            <b><font size=11 color="#1f2937">Registrado por:</font></b> {user.full_name}
            </para>
        """
        
        group_card = Table([[Paragraph(group_info, card_style)]], colWidths=[7.5*inch])
        group_card.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E5E7EB")),
            ('LEFTPADDING', (0, 0), (-1, -1), 16),
            ('RIGHTPADDING', (0, 0), (-1, -1), 16),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(group_card)
        elements.append(Spacer(1, 24))

        # ----------------------
        # DETALLE DEL GASTO (Card destacada)
        # ----------------------
        section_title = ParagraphStyle(
            "SectionTitle",
            parent=styles["Heading2"],
            textColor=colors.HexColor("#1f2937"),
            fontSize=14,
            fontName="Helvetica-Bold",
            spaceAfter=12
        )
        
        elements.append(Paragraph("Detalle del Gasto", section_title))

        # Monto destacado
        amount_style = ParagraphStyle(
            "Amount",
            parent=styles["Normal"],
            fontSize=28,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#10B981"),
            alignment=1  # Centrado
        )

        expense_data = [
            [Paragraph("<b>Descripción</b>", card_style), Paragraph(expense.title, card_style)],
            [Paragraph("<b>Monto Total</b>", card_style), Paragraph(f"<font size=18 color='#10B981'><b>${expense.amount_total:,.0f}</b></font>", card_style)],
        ]

        expense_table = Table(expense_data, colWidths=[2*inch, 5.5*inch])
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
            ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#4F46E5")),
            ('LEFTPADDING', (0, 0), (-1, -1), 16),
            ('RIGHTPADDING', (0, 0), (-1, -1), 16),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(expense_table)
        elements.append(Spacer(1, 28))

        # ----------------------
        # TABLA DE PARTICIPANTES (Moderna)
        # ----------------------
        elements.append(Paragraph("Distribución del Gasto", section_title))

        # Estilo para el header de la tabla (texto blanco)
        header_style = ParagraphStyle(
            "Header",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            textColor=colors.white,
            fontName="Helvetica-Bold"
        )

        # Header de la tabla
        table_data = [[
            Paragraph("Participante", header_style),
            Paragraph("Aporte", header_style)
        ]]

        # Filas de participantes
        for p in participants:
            table_data.append([
                Paragraph(p["name"], card_style),
                Paragraph(f"<b>${p['contribution']:,.0f}</b>", card_style)
            ])

        participants_table = Table(table_data, colWidths=[5*inch, 2.5*inch])
        participants_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Filas alternas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
            
            # Bordes
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E5E7EB")),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor("#4F46E5")),
            ('GRID', (0, 1), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            # Alineación
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(participants_table)
        elements.append(Spacer(1, 30))

        # ----------------------
        # FOOTER
        # ----------------------
        footer_style = ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#9CA3AF"),
            alignment=1  # Centrado
        )
        
        elements.append(Paragraph(
            "Gracias por usar DiviPay 💙 • Gestión inteligente de gastos compartidos",
            footer_style
        ))

        # Construcción del PDF
        doc.build(elements)

        buffer.seek(0)
        return buffer
