import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_report_cards(file_name):
    try:
        # Step 1: Read the Excel file
        df = pd.read_excel(file_name)

        # Validate required columns
        required_columns = {'Student ID', 'Name', 'Subject', 'Score'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Missing required columns. Expected: {required_columns}")

        # Step 2: Group data by student
        grouped = df.groupby(['Student ID', 'Name'])

        for (student_id, student_name), group in grouped:
            # Calculate total and average score
            total_score = group['Score'].sum()
            average_score = group['Score'].mean()

            # Create a table of subject-wise scores
            subject_scores = [['Subject', 'Score']] + group[['Subject', 'Score']].values.tolist()

            # Step 3: Generate a PDF report card
            file_path = f"report_card_{student_id}.pdf"
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            title = Paragraph(f"Report Card - {student_name}", styles['Title'])
            elements.append(title)

            summary = Paragraph(f"<b>Total Score:</b> {total_score}<br/><b>Average Score:</b> {average_score:.2f}", styles['Normal'])
            elements.append(summary)

            # Add subject-wise scores table
            table = Table(subject_scores)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ]))
            elements.append(table)

            doc.build(elements)

            print(f"Generated report card for {student_name}: {file_path}")

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Usage
if __name__ == "__main__":
    generate_report_cards("student_scores.xlsx")
