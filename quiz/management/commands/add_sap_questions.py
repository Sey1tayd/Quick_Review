from django.core.management.base import BaseCommand
from django.db.models import Max
from quiz.models import Course, Session, Question, Choice
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Adds questions for SAP'

    def handle(self, *args, **options):
        # Create or get course
        course, created = Course.objects.get_or_create(
            slug='sap',
            defaults={'title': 'SAP'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
        else:
            self.stdout.write(f'Using existing course: {course.title}')

        # Create or get session
        session_title = 'Working question set'
        session_slug = slugify(session_title)
        session, created = Session.objects.get_or_create(
            course=course,
            slug=session_slug,
            defaults={'title': session_title, 'is_published': True}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created session: {session.title}'))
        else:
            self.stdout.write(f'Using existing session: {session.title}')

        # Questions data
        questions_data = [
            {
                'text': 'What is the main purpose of ABAP in an SAP system?',
                'choices': [
                    ('To manage database backups', False),
                    ('To develop custom business logic, reports, forms, and interfaces', True),
                    ('To configure company codes and controlling areas', False),
                    ('To monitor hardware performance', False),
                ]
            },
            {
                'text': 'Which transaction is primarily used to create or edit an executable ABAP program (report)?',
                'choices': [
                    ('SE11', False),
                    ('SE16N', False),
                    ('SE38', True),
                    ('SE37', False),
                ]
            },
            {
                'text': 'In ABAP, what is an internal table?',
                'choices': [
                    ('A database table stored on the server', False),
                    ('A temporary table in application memory used to hold multiple rows of data', True),
                    ('A fixed constant value', False),
                    ('A special kind of BAdI implementation', False),
                ]
            },
            {
                'text': 'In the debugger, which key do you use to execute the current line and move to the next one (step into)?',
                'choices': [
                    ('F3', False),
                    ('F5', True),
                    ('F6', False),
                    ('F8', False),
                ]
            },
            {
                'text': 'What does this program do? (DATA: lt_mara TYPE TABLE OF mara... SELECT * FROM mara... LOOP AT lt_mara... WRITE: / ls_mara-matnr...)',
                'choices': [
                    ('Deletes 5 materials from MARA', False),
                    ('Updates 5 materials with new numbers', False),
                    ('Reads up to 5 materials from MARA and prints their numbers', True),
                    ('Creates 5 new material records', False),
                ]
            },
            {
                'text': 'What is the main purpose of SAP BW?',
                'choices': [
                    ('To execute business transactions (create orders, post invoices)', False),
                    ('To store configuration settings', False),
                    ('To provide a data warehouse for reporting and analytics', True),
                    ('To manage user authorizations', False),
                ]
            },
            {
                'text': 'Which BW object is used to store detailed transactional data?',
                'choices': [
                    ('InfoObject', False),
                    ('ADSO', True),
                    ('Query', False),
                    ('Transformation', False),
                ]
            },
            {
                'text': 'Which one is typically closest to the end user?',
                'choices': [
                    ('DataSource', False),
                    ('ADSO', False),
                    ('CompositeProvider', False),
                    ('Query', True),
                ]
            },
            {
                'text': 'In a typical BW flow, which of the following is the correct order?',
                'choices': [
                    ('Query → DataSource → ADSO → CompositeProvider', False),
                    ('DataSource → ADSO → CompositeProvider → Query', True),
                    ('ADSO → DataSource → Query → CompositeProvider', False),
                    ('CompositeProvider → DataSource → ADSO → Query', False),
                ]
            },
            {
                'text': 'What is an InfoObject in BW?',
                'choices': [
                    ('A frontend reporting tool', False),
                    ('A basic building block like Customer, Material, Amount used in all BW objects', True),
                    ('A background job', False),
                    ('A type of authorization object', False),
                ]
            },
            {
                'text': 'Which ERP transaction code is the main place to maintain all extractor settings (typically 2LIS_*), including setup/delta behavior?',
                'choices': [
                    ('RSA5', False),
                    ('RSA6', False),
                    ('LBWE', True),
                    ('RSA1', False),
                ]
            },
            {
                'text': 'In ERP, which transaction code is most commonly used to list and activate delivered/available DataSources in the OLTP system?',
                'choices': [
                    ('RSA5', True),
                    ('LBWE', False),
                    ('RSA1', False),
                    ('SM37', False),
                ]
            },
            {
                'text': 'On the BW side, which transaction code is the central workbench for Source System, DataSource replication, Transformations/DTPs, and Process Chains?',
                'choices': [
                    ('RSA1', True),
                    ('RSA5', False),
                    ('LBWE', False),
                    ('SM37', False),
                ]
            },
            {
                'text': 'Which of the following statements best describes the role of the General Ledger (GL) in SAP FI?',
                'choices': [
                    ('It stores only vendor and customer-level details.', False),
                    ('It summarizes financial postings from subledgers through reconciliation accounts.', True),
                    ('It is used only for internal reporting and management decisions.', False),
                    ('It handles production orders and material movements.', False),
                ]
            },
            {
                'text': 'In the AP process, when a vendor invoice is posted, what happens in the system?',
                'choices': [
                    ('The vendor account is debited and the expense account is credited.', False),
                    ('The vendor account is credited and the relevant expense or asset account is debited.', True),
                    ('The vendor account remains unchanged until payment is made.', False),
                    ('The payment is posted automatically without any manual steps.', False),
                ]
            },
            {
                'text': 'Which SAP tables are updated when a user posts a vendor invoice using T-Code FB60?',
                'choices': [
                    ('BKPF and BSEG', True),
                    ('BSIK and BSEG', False),
                    ('BKPF, BSEG, LFA1 and BSIK', False),
                    ('BKPF, ANLA, ANLC', False),
                ]
            },
            {
                'text': 'Which statement best describes the purpose of Profitability Analysis (CO-PA) in SAP?',
                'choices': [
                    ('It analyzes profitability based on multiple dimensions like customer, material, and sales organization.', True),
                    ('It only tracks internal costs for production resources.', False),
                    ('It is used only for external financial reporting.', False),
                    ('It calculates asset depreciation values.', False),
                ]
            },
            {
                'text': 'Based on the cost center hierarchy slide, which of the following is TRUE?',
                'choices': [
                    ('A cost center represents a product meant for customer delivery.', False),
                    ('Cost centers are grouped under organizational areas like Logistics, Administration, or Production.', True),
                    ('Cost centers track profitability.', False),
                    ('Cost centers always require revenue postings.', False),
                ]
            },
            {
                'text': 'In the Internal Orders process (Real Order → CWIP → Asset), what is the role of the periodic settlement?',
                'choices': [
                    ('It finalizes depreciation calculation.', False),
                    ('It transfers accumulated costs from the internal order to a CWIP asset.', True),
                    ('It posts revenues to the profit center.', False),
                    ('It replaces the FI posting step.', False),
                ]
            },
            {
                'text': 'Which of the following is NOT part of SAP PP master data?',
                'choices': [
                    ('Bill of Materials (BOM)', False),
                    ('Work Center', False),
                    ('Routing', False),
                    ('Sales Scheduling Agreement', True),
                ]
            },
            {
                'text': 'What is the primary purpose of a Routing in SAP PP?',
                'choices': [
                    ('To store all components required to build a product', False),
                    ('To define step-by-step operations needed to manufacture a product', True),
                    ('To assign vendors to materials', False),
                    ('To record goods movements in inventory', False),
                ]
            },
            {
                'text': 'In a Routing, which object identifies where an operation will be performed?',
                'choices': [
                    ('Bill of Materials (BOM)', False),
                    ('Work Center', True),
                    ('Material Master', False),
                    ('Production Version', False),
                ]
            },
            {
                'text': 'Which statement best describes a Routing?',
                'choices': [
                    ('It defines all components required to manufacture a product', False),
                    ('It defines the sequence of production operations and the work centers involved', True),
                    ('It defines the warehouse routes for internal stock movements', False),
                    ('It calculates prices based on customer requirements', False),
                ]
            },
            {
                'text': 'Which PP object determines the list of required components and their quantities for production?',
                'choices': [
                    ('Work Center', False),
                    ('MRP Area', False),
                    ('BOM', True),
                    ('Production Version', False),
                ]
            },
            {
                'text': 'Which of the following is a key function of a Work Center?',
                'choices': [
                    ('Stores alternative material components', False),
                    ('Provides pricing data for sales documents', False),
                    ('Holds machine time, labor capacity, and cost calculation data', True),
                    ('Determines delivery dates for customers', False),
                ]
            },
            {
                'text': 'What is the main purpose of Master Production Scheduling (MPS)?',
                'choices': [
                    ('To create purchase orders for all materials', False),
                    ('To focus planning on critical or high-profit products', True),
                    ('To automatically close all production orders', False),
                    ('To manage warehouse operations', False),
                ]
            },
            {
                'text': 'After MPS creates production orders, which process continues the planning?',
                'choices': [
                    ('Direct billing process', False),
                    ('Material Requirements Planning (MRP)', True),
                    ('Sales contract creation in SD', False),
                    ('Working hours calculation in HR', False),
                ]
            },
            {
                'text': 'Which production type is most suitable for industries like pharmaceuticals or chemicals?',
                'choices': [
                    ('Discrete Manufacturing', False),
                    ('Repetitive Manufacturing', False),
                    ('Process Manufacturing', True),
                    ('Production Planning', False),
                ]
            },
            {
                'text': 'In which production type do companies create the same product continuously without frequent changes?',
                'choices': [
                    ('Repetitive Manufacturing', True),
                    ('Discrete Manufacturing', False),
                    ('Process Manufacturing', False),
                    ('Sales & Distribution', False),
                ]
            },
            {
                'text': 'Which production type is used for "high-volume, long-term, and repetitive manufacturing of the same product"?',
                'choices': [
                    ('Make-to-Order (MTO)', False),
                    ('Repetitive Manufacturing', True),
                    ('Discrete Manufacturing', False),
                    ('Kanban Production', False),
                ]
            },
            {
                'text': 'Which PP transaction code is used to create a production order?',
                'choices': [
                    ('MD04', False),
                    ('CO01', True),
                    ('CS01', False),
                    ('CA02', False),
                ]
            },
            {
                'text': 'The table STPO is mainly used to store which type of information?',
                'choices': [
                    ('Work center capacity', False),
                    ('Routing operation details', False),
                    ('BOM item components', True),
                    ('Production order header data', False),
                ]
            },
            {
                'text': 'Which combination below is correct for PP master data?',
                'choices': [
                    ('CR01 → BOM creation; MARA → Work center data', False),
                    ('CS01 → BOM creation; CRHD → Work center data', True),
                    ('MD02 → Routing creation; AFKO → Routing header', False),
                    ('CO02 → MRP run; STKO → Planning table', False),
                ]
            },
            {
                'text': 'Which of the following is a direct responsibility of the Accounts Receivable module?',
                'choices': [
                    ('Managing depreciation and asset retirement', False),
                    ('Posting incoming customer payments and clearing open receivables', True),
                    ('Recording inventory movements from warehouses', False),
                    ('Monitoring planned vs actual production costs', False),
                ]
            },
            {
                'text': 'What is the primary purpose of depreciation in the Asset Accounting module?',
                'choices': [
                    ('To update material master data', False),
                    ('To reduce vendor liabilities', False),
                    ("To systematically allocate the asset's value as an expense over time", True),
                    ('To calculate internal sales revenue', False),
                ]
            },
            {
                'text': 'What does this program do? (DATA: lt_mara TYPE TABLE OF mara, ls_mara TYPE mara. SELECT * FROM mara INTO TABLE lt_mara UP TO 5 ROWS. LOOP AT lt_mara INTO ls_mara. WRITE: / ls_mara-matnr. ENDLOOP.)',
                'choices': [
                    ('Deletes 5 materials from MARA', False),
                    ('Updates 5 materials with new numbers', False),
                    ('Reads up to 5 materials from MARA and prints their numbers', True),
                    ('Creates 5 new material records', False),
                ]
            },
        ]

        # Get the maximum order number for existing questions in this session
        max_order = Question.objects.filter(session=session).aggregate(
            max_order=Max('order')
        )['max_order'] or 0

        # Add questions
        added_count = 0
        for idx, q_data in enumerate(questions_data, start=1):
            order = max_order + idx
            
            # Check if question already exists (by text)
            question, created = Question.objects.get_or_create(
                session=session,
                text=q_data['text'],
                defaults={'order': order, 'is_active': True}
            )
            
            if created:
                # Add choices
                for choice_text, is_correct in q_data['choices']:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
                added_count += 1
                # Safe encoding for display - encode to ASCII with errors replaced
                try:
                    display_text = q_data["text"][:50].encode('ascii', errors='replace').decode('ascii')
                except:
                    display_text = f"Question {idx}"
                self.stdout.write(f'  Added question {idx}: {display_text}...')
            else:
                # Safe encoding for display - encode to ASCII with errors replaced
                try:
                    display_text = q_data["text"][:50].encode('ascii', errors='replace').decode('ascii')
                except:
                    display_text = f"Question {idx}"
                self.stdout.write(f'  Question {idx} already exists: {display_text}...')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(questions_data)} questions. '
                f'{added_count} new questions added, {len(questions_data) - added_count} already existed.'
            )
        )
