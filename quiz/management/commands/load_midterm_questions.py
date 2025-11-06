from django.core.management.base import BaseCommand
from quiz.models import Course, Session, Question, Choice


class Command(BaseCommand):
    help = 'Load COMP3003 Midterm questions into the database'

    def handle(self, *args, **options):
        # Create or get course
        course, created = Course.objects.get_or_create(
            slug='COMP3003',
            defaults={
                'title': 'COMP3003 Software Engineering',
                'description': 'Software Engineering course questions covering software development methodologies, agile practices, and requirements engineering.'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
        else:
            self.stdout.write(f'Course already exists: {course.title}')

        # Create Midterm session
        session, created = Session.objects.get_or_create(
            course=course,
            slug='midterm',
            defaults={
                'title': 'Midterm',
                'is_published': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created session: {session.title}'))
        else:
            self.stdout.write(f'Session already exists: {session.title}')

        # All questions for Midterm (91 questions total - duplicates removed)
        questions = [
            {
                'text': 'What is a key advantage of software inspections as a verification technique compared to dynamic testing?',
                'choices': [
                    ('Inspections can prove that a program is 100% free of defects.', False),
                    ('Inspections can check non-functional characteristics such as system performance and usability.', False),
                    ('Inspections are dynamic and involve executing the code with test data.', False),
                    ('Incomplete versions of a system can be inspected without needing to write test harnesses, and one error does not mask the presence of another.', True),
                ],
                'feedback': 'Because inspections are static, you don\'t need an executable program, and the flow of execution can\'t hide a downstream bug.'
            },
            {
                'text': 'What is the main purpose of context models in system modeling?',
                'choices': [
                    ('To detail internal data processing only.', False),
                    ('To generate code implementations.', False),
                    ('To model dynamic behaviors exclusively.', False),
                    ('To illustrate the operational context of a system and show what lies outside its boundaries.', True),
                ],
                'feedback': 'Context models illustrate the operational context of a system and show what lies outside its boundaries.'
            },
            {
                'text': 'Agile methods are most successful for small, co-located teams. Which factor makes scaling these methods to large systems difficult?',
                'choices': [
                    ('The difficulty in maintaining documentation and development team continuity over a long system lifetime', True),
                    ('The requirement for only highly-skilled and experienced programmers', False),
                    ('The inability to perform incremental delivery with large software products', False),
                    ('The lack of any tools to support continuous integration', False),
                ],
                'feedback': 'Long-lifetime systems require documentation, and team turnover over a long procurement/development time is a major challenge for agile\'s minimal documentation approach.'
            },
            {
                'text': 'A core benefit of **Test-first development** in agile methods is that it:',
                'choices': [
                    ('Allows the final user acceptance tests to be written by the development team alone', False),
                    ('Reduces the project\'s reliance on automated testing tools', False),
                    ('Eliminates the need for any further system-level or acceptance testing', False),
                    ('Clarifies the requirements that need to be implemented', True),
                ],
                'feedback': 'Writing tests before the code itself helps clarify exactly what the new functionality is intended to do, ensuring it meets the requirements.'
            },
            {
                'text': 'What are the two primary, distinct goals of program testing?',
                'choices': [
                    ('To prove that the software has no errors and to write user documentation.', False),
                    ('To run the program on a host machine and to run it on a target machine.', False),
                    ('To demonstrate that the software meets its requirements (validation) and to discover incorrect behavior (defect testing).', True),
                    ('To test individual components (unit testing) and to test the integrated system (system testing).', False),
                ],
                'feedback': 'Testing has two main goals: 1) Validation testing, which demonstrates to the developer and customer that the software meets its requirements, and 2) Defect testing, which aims to discover situations where the software\'s behavior is incorrect or does not conform to its specification.'
            },
            {
                'text': 'Which characteristic ensures that a dependable process can be audited by external parties?',
                'choices': [
                    ('Auditable, meaning it is understandable and allows checking of standards', True),
                    ('Diverse', False),
                    ('Robust', False),
                    ('Repeatable', False),
                ],
                'feedback': 'Auditable means the process is understandable and allows checking of standards.'
            },
            {
                'text': 'Which option correctly distinguishes functional requirements from non-functional requirements?',
                'choices': [
                    ('Functional requirements are always measurable while non-functional requirements are always subjective.', False),
                    ('Functional requirements describe specific services or functions the system must provide; non-functional requirements constrain qualities like performance, reliability, security and usability.', True),
                    ('Functional requirements describe the user interface exclusively; non-functional requirements describe database tables exclusively.', False),
                    ('Functional requirements state corporate policies while non-functional requirements only list hardware components.', False),
                ],
                'feedback': 'Functional requirements describe specific services or functions the system must provide; non-functional requirements constrain qualities like performance, reliability, security and usability.'
            },
            {
                'text': 'What is a key difference between system testing done by the development team and release testing?',
                'choices': [
                    ('There is no difference; they are two names for the same process.', False),
                    ('Release testing is done before unit testing and component testing.', False),
                    ('System testing is only done by users, while release testing is done by developers.', False),
                    ('Release testing is a validation-focused process (checking requirements) often done by a separate team, while development system testing is a defect-focused process (finding bugs).', True),
                ],
                'feedback': 'System testing by the development team focuses on discovering bugs (defect testing). Release testing is done by a separate team to check that the system meets its requirements and is good enough for external use (validation testing). Release testing is usually a black-box process.'
            },
            {
                'text': 'What does the dependability of a computer-based system primarily reflect?',
                'choices': [
                    ('The system\'s processing speed', False),
                    ('The user\'s degree of trust that the system will operate as expected without failing in normal use', True),
                    ('The number of users accessing the system', False),
                    ('The cost of hardware components', False),
                ],
                'feedback': 'Dependability reflects the user\'s degree of trust that the system will operate as expected without failing in normal use.'
            },
            {
                'text': 'Which of the following is a common architectural view mentioned in software architecture documentation?',
                'choices': [
                    ('Texture view.', False),
                    ('Color view.', False),
                    ('Process view.', True),
                    ('Sound view.', False),
                ],
                'feedback': 'Process view is a common architectural view in software architecture documentation.'
            },
            {
                'text': 'What is an architectural pattern?',
                'choices': [
                    ('A detailed user requirement specification.', False),
                    ('A stylized description of good design practice that has been tried and tested in different environments.', True),
                    ('A specific code implementation for a module.', False),
                    ('A testing strategy for system validation.', False),
                ],
                'feedback': 'An architectural pattern is a stylized description of good design practice that has been tried and tested in different environments.'
            },
            {
                'text': 'Which UML diagram type is used to show the activities involved in a process or data processing?',
                'choices': [
                    ('Use case diagrams.', False),
                    ('Sequence diagrams.', False),
                    ('Class diagrams.', False),
                    ('Activity diagrams.', True),
                ],
                'feedback': 'Activity diagrams are used to show the activities involved in a process or data processing.'
            },
            {
                'text': 'In Extreme Programming (XP), which of the following is a primary benefit of **Pair Programming**?',
                'choices': [
                    ('Reducing the total working hours required for a software release', False),
                    ('Ensuring strict separation of duties between developers', False),
                    ('Limiting the number of people who can change a specific part of the code', False),
                    ('Spreading knowledge of the system across the development team', True),
                ],
                'feedback': 'Pair programming helps spread system knowledge across the team and serves as an immediate, informal code review.'
            },
            {
                'text': 'Why do maintenance costs often exceed development costs for software systems?',
                'choices': [
                    ('Structure degrades over time, requiring more effort for changes, and maintenance staff may lack domain knowledge', True),
                    ('Costs decrease with software age', False),
                    ('Maintenance avoids any testing', False),
                    ('Development is always cheaper due to automation', False),
                ],
                'feedback': 'Structure degrades over time, requiring more effort for changes, and maintenance staff may lack domain knowledge.'
            },
            {
                'text': 'When is the classic waterfall model generally most appropriate?',
                'choices': [
                    ('When only UI prototypes are required', False),
                    ('When requirements are stable and well understood', True),
                    ('When no documentation is desired', False),
                    ('When rapid, continuous requirement changes are expected', False),
                ],
                'feedback': 'The waterfall model fits stable, well-understood requirements.'
            },
            {
                'text': 'Which of the following is a common approach used for object class identification during object-oriented design?',
                'choices': [
                    ('Running the final program and seeing what objects are created in memory.', False),
                    ('Using a grammatical approach based on a natural language description of the system.', True),
                    ('A \'magic formula\' that provides the correct classes on the first try.', False),
                    ('Copying the object classes from an unrelated project.', False),
                ],
                'feedback': 'Common approaches to identifying object classes include: using a grammatical approach on a natural language description (nouns often become objects), basing identification on tangible things in the application domain, and using scenario-based analysis.'
            },
            {
                'text': 'Design models are broadly categorized into two main types. What do these two types describe?',
                'choices': [
                    ('Physical models describe the hardware, while logical models describe the software.', False),
                    ('Use-case models describe user actions, while subsystem models describe logical groupings.', False),
                    ('Structural models describe the static structure of the system, while dynamic models describe the dynamic interactions between objects.', True),
                    ('Implementation models describe the code, while design models describe the abstractions.', False),
                ],
                'feedback': 'The two kinds of design models are structural models, which describe the static structure of the system (like object classes and relationships), and dynamic models, which describe the dynamic interactions between objects.'
            },
            {
                'text': 'Which pair correctly names two broad approaches to software process improvement?',
                'choices': [
                    ('Database-centric and UI-centric', False),
                    ('Waterfall approach and debugging approach', False),
                    ('DevOps only and documentation-first only', False),
                    ('Process maturity approach and agile approach', True),
                ],
                'feedback': 'Process maturity approach and agile approach are two broad approaches to software process improvement.'
            },
            {
                'text': 'Which is a key benefit of incremental development?',
                'choices': [
                    ('No testing at early stages', False),
                    ('Earlier delivery of useful functionality with easier customer feedback', True),
                    ('Full specification frozen before any coding', False),
                    ('Complete elimination of refactoring', False),
                ],
                'feedback': 'Incremental development reduces the cost of accommodating change and enables earlier delivery and feedback.'
            },
            {
                'text': 'What is the typical output of the architectural design process?',
                'choices': [
                    ('Detailed user interface prototypes.', False),
                    ('A list of test cases for the system.', False),
                    ('An architectural model describing the system as a set of communicating components.', True),
                    ('A complete source code implementation.', False),
                ],
                'feedback': 'The typical output of architectural design is an architectural model describing the system as a set of communicating components.'
            },
            {
                'text': 'The Extreme Programming (XP) practice of **Refactoring** primarily involves:',
                'choices': [
                    ('Anticipating future changes and designing the system architecture to accommodate them', False),
                    ('Continuously restructuring and improving the software code to keep it simple and maintainable', True),
                    ('Redeveloping the entire system architecture once a year to reflect new technologies', False),
                    ('Writing new unit tests after a new piece of functionality has been completely implemented', False),
                ],
                'feedback': 'Refactoring is the continuous process of improving the code structure and clarity without changing its external behavior, making future changes easier.'
            },
            {
                'text': 'Which statement best captures the primary goal of requirements engineering?',
                'choices': [
                    ('A technique for modeling database schemas only.', False),
                    ('An approach to performance tuning and deployment after release.', False),
                    ('The process of discovering, documenting and maintaining the services a system should provide and the constraints on its operation and development.', True),
                    ('The phase where all system source code is written and integrated.', False),
                ],
                'feedback': 'Requirements engineering is the process of discovering, documenting and maintaining the services a system should provide and the constraints on its operation and development.'
            },
            {
                'text': 'What is a well-known drawback of the waterfall model?',
                'choices': [
                    ('Absence of documentation', False),
                    ('Difficulty accommodating change once phases progress', True),
                    ('Excessive customer involvement', False),
                    ('No testing phase', False),
                ],
                'feedback': 'Accommodating change is difficult after the process is underway in the waterfall model.'
            },
            {
                'text': 'What is the core principle of Test-Driven Development (TDD)?',
                'choices': [
                    ('All testing is driven by the user, who must approve every line of code.', False),
                    ('Tests for a new piece of functionality are written before the code is implemented, and the code is developed incrementally to pass the test.', True),
                    ('Developers are not allowed to write tests; this is handled by a separate testing team.', False),
                    ('Testing is the final phase of development, occurring only after all code is written.', False),
                ],
                'feedback': 'TDD is an approach where tests are written *before* the code. You identify a new increment of functionality, write a test for it, and run the test (which will fail). You then implement the functionality and re-run the test. You don\'t move on until all tests pass.'
            },
            {
                'text': 'The need for systems to work across diverse devices and platforms primarily highlights which issue?',
                'choices': [
                    ('Virtualization only', False),
                    ('Monoculture', False),
                    ('Gamification', False),
                    ('Heterogeneity', True),
                ],
                'feedback': 'Heterogeneity captures diversity in platforms, networks, and device types.'
            },
            {
                'text': 'In software V&V, what is the difference between verification and validation?',
                'choices': [
                    ('Verification is dynamic testing (running the code), while validation is static analysis (inspecting the code).', False),
                    ('Verification and validation are two names for the same testing process.', False),
                    ('Verification checks if the product is built right (conforms to specification), while validation checks if the right product is built (meets user requirements).', True),
                    ('Verification is done by developers, while validation is done only by customers.', False),
                ],
                'feedback': 'Verification is: "Are we building the product right?" (i.e., the software conforms to its specification). Validation is: "Are we building the right product?" (i.e., the software does what the user really requires).'
            },
            {
                'text': 'What is the primary purpose of a UML state diagram (or state machine model)?',
                'choices': [
                    ('To show how a single object changes its state in response to events.', True),
                    ('To show the sequence of interactions between multiple objects over time.', False),
                    ('To describe the static, structural organization of all classes in the system.', False),
                    ('To show the logical groupings of objects into coherent subsystems.', False),
                ],
                'feedback': 'State diagrams are used to show how individual objects respond to different service requests (events) and the state transitions triggered by these requests. They are useful high-level models of an object\'s run-time behavior.'
            },
            {
                'text': 'Which set lists activities typically included in requirements engineering?',
                'choices': [
                    ('Design; coding; debugging', False),
                    ('Prototyping; unit testing; deployment', False),
                    ('Elicitation & analysis; specification; validation', True),
                    ('Hiring; training; procurement', False),
                ],
                'feedback': 'Elicitation & analysis, specification, and validation are core activities in requirements engineering.'
            },
            {
                'text': 'What does a sociotechnical system encompass beyond just software?',
                'choices': [
                    ('Business processes alone', False),
                    ('Hardware, people, organizations, and societal factors like laws and culture', True),
                    ('Only software code', False),
                    ('Isolated hardware components', False),
                ],
                'feedback': 'A sociotechnical system encompasses hardware, people, organizations, and societal factors like laws and culture.'
            },
            {
                'text': 'What is refactoring primarily intended to achieve in software maintenance?',
                'choices': [
                    ('Increasing method length for clarity', False),
                    ('Adding new features immediately', False),
                    ('Duplicating code for backups', False),
                    ('Improving program structure and reducing complexity to prevent future degradation', True),
                ],
                'feedback': 'Refactoring is primarily intended to improve program structure and reduce complexity to prevent future degradation.'
            },
            {
                'text': 'Unlike a plan-driven approach, the process outputs (deliverables) in agile development are:',
                'choices': [
                    ('Decided through a process of continuous negotiation during development', True),
                    ('Completely undocumented and not formally reviewed by stakeholders', False),
                    ('Planned in detail before the project\'s implementation phase begins', False),
                    ('Identical to those produced in a waterfall model', False),
                ],
                'feedback': 'Plan-driven approaches define outputs in advance, but in agile, outputs are decided throughout the process via negotiation.'
            },
            {
                'text': 'Which statement best contrasts plan-driven and agile processes?',
                'choices': [
                    ('Both forbid change once coding starts', False),
                    ('Plan-driven never uses schedules', False),
                    ('Plan-driven plans activities up front; agile uses incremental planning to adapt', True),
                    ('Agile requires full documentation before coding', False),
                ],
                'feedback': 'Plan-driven plans up front; agile plans incrementally to accommodate change.'
            },
            {
                'text': 'Why are multiple architectural views typically needed for a system?',
                'choices': [
                    ('To limit the documentation to a single diagram.', False),
                    ('To focus solely on runtime behavior.', False),
                    ('To avoid using notations like UML.', False),
                    ('Each view shows only one perspective, such as module decomposition or process interactions.', True),
                ],
                'feedback': 'Multiple architectural views are needed because each view shows only one perspective, such as module decomposition or process interactions.'
            },
            {
                'text': 'What do process models reveal about a system being developed?',
                'choices': [
                    ('Only the internal class structures.', False),
                    ('Hardware platform specifics.', False),
                    ('External environmental factors exclusively.', False),
                    ('How the system is used in broader business processes.', True),
                ],
                'feedback': 'Process models reveal how the system is used in broader business processes.'
            },
            {
                'text': 'Why is dependability crucial for critical systems?',
                'choices': [
                    ('System failures can lead to economic losses, physical damage, or threats to human life', True),
                    ('To increase marketing appeal', False),
                    ('To reduce development time', False),
                    ('For aesthetic design purposes', False),
                ],
                'feedback': 'Dependability is crucial for critical systems because system failures can lead to economic losses, physical damage, or threats to human life.'
            },
            {
                'text': 'When using graphical models to facilitate discussion about a proposed system, what is acceptable regarding the models?',
                'choices': [
                    ('They need to be accurate but not complete.', False),
                    ('They should only represent final implementations.', False),
                    ('They can be incomplete and incorrect as their role is to support discussion.', True),
                    ('They must be both correct and complete.', False),
                ],
                'feedback': 'Graphical models used for discussion can be incomplete and incorrect as their role is to support discussion and facilitate understanding.'
            },
            {
                'text': 'What do use case diagrams primarily illustrate in system modeling?',
                'choices': [
                    ('System reactions to internal events only.', False),
                    ('Data processing sequences.', False),
                    ('Object classes and their associations.', False),
                    ('Interactions between a system and its environment.', True),
                ],
                'feedback': 'Use case diagrams primarily illustrate interactions between a system and its environment.'
            },
            {
                'text': 'What is the primary purpose of system modeling in software engineering?',
                'choices': [
                    ('To develop abstract models of a system, each presenting a different view or perspective.', True),
                    ('To write executable code directly from requirements.', False),
                    ('To perform hardware simulations.', False),
                    ('To manage project timelines exclusively.', False),
                ],
                'feedback': 'The primary purpose of system modeling is to develop abstract models of a system, each presenting a different view or perspective.'
            },
            {
                'text': 'In Scrum, the primary responsibility of the **ScrumMaster** is to:',
                'choices': [
                    ('Ensure the Scrum process is followed and protect the development team from external interference', True),
                    ('Be the technical lead responsible for the entire system architecture design', False),
                    ('Be the full-time representative of the end-user (the customer)', False),
                    ('Define product features and prioritize the Product Backlog', False),
                ],
                'feedback': 'The ScrumMaster ensures the process is followed, guides the team, and protects them from outside interference.'
            },
            {
                'text': 'What is the purpose of using diversity in system design for dependability?',
                'choices': [
                    ('To duplicate exact copies only', False),
                    ('To reduce overall functionality', False),
                    ('To increase system complexity unnecessarily', False),
                    ('To provide the same functionality in different ways to avoid common-mode failures', True),
                ],
                'feedback': 'Diversity in system design provides the same functionality in different ways to avoid common-mode failures.'
            },
            {
                'text': 'Which statement best describes the relationship between software design and implementation?',
                'choices': [
                    ('Implementation is the process of defining customer requirements, and design is the process of writing code.', False),
                    ('Design is a creative activity of identifying components, and implementation is the process of realizing the design as a program; the two activities are often inter-leaved.', True),
                    ('A complete and final design must be 100% finished before any implementation can begin.', False),
                    ('Design and implementation are two different terms for the exact same activity.', False),
                ],
                'feedback': 'Software design is the creative activity of identifying components and their relationships, while implementation is the process of realizing that design as an executable program. These activities are often inter-leaved.'
            },
            {
                'text': 'Which of the following is a principal dependability property defined as the probability that a system will be operational and deliver services when needed?',
                'choices': [
                    ('Security', False),
                    ('Safety', False),
                    ('Reliability', False),
                    ('Availability', True),
                ],
                'feedback': 'Availability is defined as the probability that a system will be operational and deliver services when needed.'
            },
            {
                'text': 'What is the most common graphical notation used for representing systems in modern system modeling?',
                'choices': [
                    ('Entity-Relationship diagrams only.', False),
                    ('Pseudocode representations.', False),
                    ('Notations based on the Unified Modeling Language (UML).', True),
                    ('Flowcharts from structured programming.', False),
                ],
                'feedback': 'The most common graphical notation used for representing systems in modern system modeling is based on the Unified Modeling Language (UML).'
            },
            {
                'text': 'In agile processes, when is it generally accepted to design the overall system architecture?',
                'choices': [
                    ('At an early stage.', True),
                    ('During the final deployment phase.', False),
                    ('Only if refactoring is needed.', False),
                    ('After all iterations are complete.', False),
                ],
                'feedback': 'In agile processes, the overall system architecture is generally designed at an early stage.'
            },
            {
                'text': 'Which action is NOT part of a sensible requirements change management process?',
                'choices': [
                    ('Automatically accepting all requested changes without impact analysis.', True),
                    ('Assessing the impact, cost and schedule implications of a requested change using traceability links.', False),
                    ('Prioritising and deciding which changes should be implemented based on business value and risk.', False),
                    ('Updating requirements artifacts and notifying affected stakeholders when a change is approved.', False),
                ],
                'feedback': 'Automatically accepting all requested changes without impact analysis is NOT part of a sensible requirements change management process.'
            },
            {
                'text': 'What is the primary reason organizations invest heavily in software evolution?',
                'choices': [
                    ('To comply with legal standards exclusively', False),
                    ('For marketing new features only', False),
                    ('To maintain the value of critical business assets through updates and changes', True),
                    ('To reduce initial development costs', False),
                ],
                'feedback': 'The primary reason organizations invest heavily in software evolution is to maintain the value of critical business assets through updates and changes.'
            },
            {
                'text': 'What is required for regulated critical systems before they can go into service?',
                'choices': [
                    ('No documentation required', False),
                    ('User feedback surveys', False),
                    ('Internal team approval only', False),
                    ('Approval from an external regulator based on a safety and dependability case', True),
                ],
                'feedback': 'Regulated critical systems require approval from an external regulator based on a safety and dependability case before they can go into service.'
            },
            {
                'text': 'In a UML sequence model, how is the flow of time represented?',
                'choices': [
                    ('Vertically, from the top of the diagram to the bottom.', True),
                    ('With timestamps explicitly written on each interaction arrow.', False),
                    ('Horizontally, from the left side of the diagram to the right.', False),
                    ('Time is not represented; sequence models are static.', False),
                ],
                'feedback': 'Sequence models show the sequence of object interactions. Objects are arranged horizontally across the top, and time is represented vertically, so the models are read from top to bottom.'
            },
            {
                'text': 'What is architectural design primarily concerned with in software engineering?',
                'choices': [
                    ('Writing detailed code for system components.', False),
                    ('Understanding how a software system should be organized and designing its overall structure.', True),
                    ('Testing the functionality of individual modules.', False),
                    ('Managing project schedules and budgets.', False),
                ],
                'feedback': 'Architectural design is primarily concerned with understanding how a software system should be organized and designing its overall structure.'
            },
            {
                'text': 'What is the primary purpose of regression testing?',
                'choices': [
                    ('To check that new changes to the software have not inadvertently \'broken\' previously working functionality.', True),
                    ('To have users test the system in their own environment.', False),
                    ('To test a new system from scratch for the first time.', False),
                    ('To test the system\'s performance and reliability under heavy load.', False),
                ],
                'feedback': 'Regression testing is testing the system to check that changes (like bug fixes or new features) have not \'broken\' previously working code. With automated testing, this involves re-running all existing tests every time a change is made.'
            },
            {
                'text': 'Which property makes a non-functional requirement verifiable?',
                'choices': [
                    ('The requirement includes measurable criteria or an objective test (for example, a specific throughput, latency bound, or error rate) so it can be checked.', True),
                    ('The requirement is written as a vague wish like "the system should be fast" without numbers.', False),
                    ('Only functional requirements can be verified; non-functional ones cannot.', False),
                    ('Verifiability requires specifying the implementation language rather than measurable tests.', False),
                ],
                'feedback': 'The requirement includes measurable criteria or an objective test (for example, a specific throughput, latency bound, or error rate) so it can be checked.'
            },
            {
                'text': 'Software engineering is best described as an engineering discipline concerned with:',
                'choices': [
                    ('All aspects of software production from specification to maintenance', True),
                    ('Only project management', False),
                    ('Only programming and debugging', False),
                    ('Only user interface design', False),
                ],
                'feedback': 'Software engineering spans specification, development, validation, and evolution.'
            },
            {
                'text': 'What is the "equivalence partitioning" testing strategy?',
                'choices': [
                    ('Forcing the system to generate all possible error messages.', False),
                    ('Testing every single possible input value to ensure 100% coverage.', False),
                    ('Testing software with sequences of zero length.', False),
                    ('Identifying groups of inputs that should be processed similarly, and choosing one test case from each group.', True),
                ],
                'feedback': 'Equivalence partitioning is a testing strategy where you identify groups (partitions) of inputs that have common characteristics and should be processed in the same way. The assumption is that if one test case from a partition works, all members of that partition will work. You should choose test cases from each partition.'
            },
            {
                'text': 'What is a key challenge in change implementation for existing software systems?',
                'choices': [
                    ('Program understanding to assess how changes affect structure and functionality', True),
                    ('Avoiding testing altogether', False),
                    ('Ignoring original developer involvement', False),
                    ('Rewriting the entire system', False),
                ],
                'feedback': 'A key challenge in change implementation is program understanding to assess how changes affect structure and functionality.'
            },
            {
                'text': 'What is the key difference between "alpha testing" and "beta testing"?',
                'choices': [
                    ('Alpha testing is automated, while beta testing is manual.', False),
                    ('Alpha testing is testing the first version of the software (A), and beta testing is testing the second version (B).', False),
                    ('Alpha testing involves users testing at the developer\'s site, while beta testing involves releasing the software to external users to test in their own environment.', True),
                    ('Alpha testing is done by developers, while beta testing is done by managers.', False),
                ],
                'feedback': 'Both are types of user testing. Alpha testing: Users of the software work with the development team to test the software at the developer\'s site. Beta testing: A release of the software is made available to users to allow them to experiment in their own environment.'
            },
            {
                'text': 'When a team decides to \'buy\' a Commercial Off-The-Shelf (COTS) system rather than \'build\' a custom one, the design process primarily shifts to what activity?',
                'choices': [
                    ('Developing a new set of requirements for a different system.', False),
                    ('Using the configuration features of the COTS system to deliver the requirements.', True),
                    ('Writing new code from scratch to replace the COTS system.', False),
                    ('Identifying all software components and their relationships from scratch.', False),
                ],
                'feedback': 'When buying a COTS system, the design process becomes concerned with how to use the configuration features of that system to deliver the system requirements. This is often cheaper and faster than building from scratch.'
            },
            {
                'text': 'Testing with real customer data to check that the system meets user needs is known as:',
                'choices': [
                    ('Integration testing only', False),
                    ('Customer (acceptance) testing', True),
                    ('Component testing', False),
                    ('Static code analysis', False),
                ],
                'feedback': 'Customer or acceptance testing validates fitness for purpose.'
            },
            {
                'text': 'How are models of an existing system typically used during requirements engineering?',
                'choices': [
                    ('To document only the final implementation details.', False),
                    ('To generate complete code implementations automatically.', False),
                    ('To clarify what the system does and discuss its strengths and weaknesses, leading to new requirements.', True),
                    ('To focus solely on hardware dependencies.', False),
                ],
                'feedback': 'Models of an existing system are used to clarify what the system does and discuss its strengths and weaknesses, leading to new requirements.'
            },
            {
                'text': 'Which of the following is an example of a testable (verifiable) usability non-functional requirement?',
                'choices': [
                    ('Users should find the interface attractive and pleasant.', False),
                    ('After four hours of training, medical staff shall be able to perform core tasks and the average number of errors by experienced users shall not exceed.', True),
                    ('Training shall be provided and usability will be determined informally.', False),
                    ('The system should be easy to use for medical staff.', False),
                ],
                'feedback': 'After four hours of training, medical staff shall be able to perform core tasks and the average number of errors by experienced users shall not exceed.'
            },
            {
                'text': 'What drives the software evolution process?',
                'choices': [
                    ('External audits', False),
                    ('Annual budget cycles only', False),
                    ('Proposals for change linked to affected components for impact estimation', True),
                    ('Random developer ideas', False),
                ],
                'feedback': 'The software evolution process is driven by proposals for change linked to affected components for impact estimation.'
            },
            {
                'text': 'In which product type does the customer typically own the specification and decide on changes?',
                'choices': [
                    ('Generic products', False),
                    ('Customized products', True),
                    ('Commercial off-the-shelf tools', False),
                    ('Open-source community projects', False),
                ],
                'feedback': 'Customized products are commissioned by a specific customer who owns the spec and change decisions.'
            },
            {
                'text': 'Which is a common challenge in incremental development if quality work is deferred?',
                'choices': [
                    ('Impossible to gather user feedback', False),
                    ('Over-documentation of every minor change', False),
                    ('Guaranteed alignment to all non-functional requirements', False),
                    ('Architecture/structure degradation unless time is invested in refactoring', True),
                ],
                'feedback': 'Without periodic refactoring, structure degrades as increments accumulate.'
            },
            {
                'text': 'Which system perspective models the dynamic behavior of the system and its responses to events?',
                'choices': [
                    ('Behavioral perspective.', True),
                    ('External perspective.', False),
                    ('Interaction perspective.', False),
                    ('Structural perspective.', False),
                ],
                'feedback': 'The behavioral perspective models the dynamic behavior of the system and its responses to events.'
            },
            {
                'text': 'What is the main goal of software reengineering?',
                'choices': [
                    ('Ignoring data inconsistencies', False),
                    ('Completely replacing the system with new code', False),
                    ('Restructuring legacy systems to improve maintainability without changing functionality', True),
                    ('Reducing all business processes', False),
                ],
                'feedback': 'The main goal of software reengineering is restructuring legacy systems to improve maintainability without changing functionality.'
            },
            {
                'text': 'According to the Agile Manifesto, which of the following is valued *more*?',
                'choices': [
                    ('Working software', True),
                    ('Following a detailed plan', False),
                    ('Contract negotiation', False),
                    ('Comprehensive documentation', False),
                ],
                'feedback': 'The Agile Manifesto emphasizes working code delivered to the customer over extensive formal documentation.'
            },
            {
                'text': 'What is a key benefit of using formal methods in dependable systems engineering?',
                'choices': [
                    ('They eliminate all testing needs', False),
                    ('They focus only on hardware', False),
                    ('They reduce specification and design errors by mathematical analysis', True),
                    ('They speed up development without analysis', False),
                ],
                'feedback': 'Formal methods reduce specification and design errors by mathematical analysis.'
            },
            {
                'text': 'Why is software change considered inevitable in software engineering?',
                'choices': [
                    ('Primarily from user dissatisfaction', False),
                    ('New requirements emerge during use, business environments change, errors need repair, and system performance may require improvement', True),
                    ('Only because of hardware failures', False),
                    ('Due to lack of developer skills', False),
                ],
                'feedback': 'Software change is inevitable because new requirements emerge during use, business environments change, errors need repair, and system performance may require improvement.'
            },
            {
                'text': 'Development testing consists of several activities. Which option correctly identifies these activities in order of increasing integration?',
                'choices': [
                    ('Static testing, Dynamic testing, and Release testing.', False),
                    ('Alpha testing, Beta testing, and Acceptance testing.', False),
                    ('System testing, Component testing, and Unit testing.', False),
                    ('Unit testing, Component testing, and System testing.', True),
                ],
                'feedback': 'Development testing includes: 1) Unit testing (individual program units or objects), 2) Component testing (integrating several units, focusing on interfaces), and 3) System testing (integrating components into a system, focusing on component interactions).'
            },
            {
                'text': 'Architectural design decisions often affect which aspects of a system?',
                'choices': [
                    ('The non-functional characteristics of the system.', True),
                    ('The detailed coding standards.', False),
                    ('Only the user interface elements.', False),
                    ('Exclusively the data storage mechanisms.', False),
                ],
                'feedback': 'Architectural design decisions often affect the non-functional characteristics of the system.'
            },
            {
                'text': 'In the Scrum agile method, the fixed-length development iteration is called a:',
                'choices': [
                    ('Velocity', False),
                    ('Scrum of Scrums', False),
                    ('Product Backlog', False),
                    ('Sprint', True),
                ],
                'feedback': 'The core development cycle in Scrum is the Sprint, which is fixed in length, usually 2-4 weeks.'
            },
            {
                'text': 'Which activity focuses on checking that the system does what the customer requires?',
                'choices': [
                    ('Software specification', False),
                    ('Software validation', True),
                    ('Software evolution', False),
                    ('Software design', False),
                ],
                'feedback': 'Validation asks "Are we building the right product?"'
            },
            {
                'text': 'What is the main goal of "stress testing"?',
                'choices': [
                    ('To test that all requirements in the specification have been met.', False),
                    ('To test each component in isolation before it is integrated.', False),
                    ('To check that the user interface is not "stressful" for new users.', False),
                    ('To deliberately overload the system to test its failure behavior.', True),
                ],
                'feedback': 'Stress testing is a form of performance testing where the system is deliberately overloaded (e.g., with many simultaneous requests) to test its failure behavior and emergent properties. It checks how the system behaves under extreme conditions.'
            },
            {
                'text': 'What factors may influence the decision on where to position system boundaries?',
                'choices': [
                    ('Purely random selections.', False),
                    ('Only technical hardware limitations.', False),
                    ('Social and organizational concerns.', True),
                    ('Exclusively user interface designs.', False),
                ],
                'feedback': 'Social and organizational concerns may influence the decision on where to position system boundaries.'
            },
            {
                'text': 'Which of the following is NOT typically considered an essential attribute of good software?',
                'choices': [
                    ('Maintainability', False),
                    ('Efficiency', False),
                    ('Dependability and security', False),
                    ('Novelty', True),
                ],
                'feedback': 'Maintainability, dependability/security, efficiency, and acceptability are classic essentials; novelty is not.'
            },
            {
                'text': 'What is the main difference between a "reciprocal" license like the GNU General Public License (GPL) and a "non-reciprocal" license like the BSD license?',
                'choices': [
                    ('The GPL applies only to the Linux kernel, while the BSD license applies only to web servers.', False),
                    ('The GPL requires systems using its code to also be open source, while the BSD license allows the code to be used in proprietary, closed-source systems.', True),
                    ('The GPL is for-profit, while the BSD license is non-profit.', False),
                    ('The GPL is a non-reciprocal license, and the BSD license is a reciprocal license.', False),
                ],
                'feedback': 'A reciprocal license (like GPL) means that if you use the open-source component, your system must also be licensed as open source. A non-reciprocal license (like BSD) does not have this restriction, allowing you to include the code in proprietary, closed-source systems.'
            },
            {
                'text': 'Which of the following is a realistic problem encountered during requirements elicitation?',
                'choices': [
                    ('Elicitation is a one-time activity; requirements do not change thereafter.', False),
                    ('Stakeholders always provide complete and precise technical specifications on the first interview.', False),
                    ('Only automated questionnaires are necessary; observation and interviews are never needed.', False),
                    ('Stakeholders may have conflicting priorities, may not be able to articulate needs clearly, or may change their minds as understanding evolves.', True),
                ],
                'feedback': 'Stakeholders may have conflicting priorities, may not be able to articulate needs clearly, or may change their minds as understanding evolves.'
            },
            {
                'text': 'Which action aligns with professional software engineering ethics?',
                'choices': [
                    ('Accepting tasks far outside one\'s competence without disclosure', False),
                    ('Copying proprietary code without permission', False),
                    ('Maintaining integrity and independence in professional judgment', True),
                    ('Sharing client data to speed up peer review', False),
                ],
                'feedback': 'Integrity/independence and respecting confidentiality and IP are core principles of professional software engineering ethics.'
            },
            {
                'text': 'Which sequence lists the SEI capability maturity levels from lowest to highest?',
                'choices': [
                    ('Repeatable → Initial → Managed → Defined → Optimizing', False),
                    ('Initial → Repeatable → Defined → Managed → Optimizing', True),
                    ('Defined → Initial → Managed → Repeatable → Optimizing', False),
                    ('Initial → Managed → Repeatable → Optimizing → Defined', False),
                ],
                'feedback': 'The classic ordering is: Initial → Repeatable → Defined → Managed → Optimizing.'
            },
            {
                'text': 'What is the fundamental purpose of a design pattern in software engineering?',
                'choices': [
                    ('To automatically generate an executable system from a description.', False),
                    ('To enforce the use of a specific programming language.', False),
                    ('To provide a complete, specific piece of code that can be copied and pasted.', False),
                    ('To provide a reusable, abstract solution to a commonly occurring problem.', True),
                ],
                'feedback': 'A design pattern is a way of reusing abstract knowledge about a problem and its solution. It is a description of the problem and the essence of its solution, sufficiently abstract to be reused in different settings.'
            },
            {
                'text': 'Which type of software maintenance involves adapting to a new operating environment?',
                'choices': [
                    ('Fault repairs', False),
                    ('Environmental adaptation', True),
                    ('System retirement', False),
                    ('Functionality addition', False),
                ],
                'feedback': 'Environmental adaptation involves adapting to a new operating environment.'
            },
            {
                'text': 'What does \'architecture in the small\' refer to?',
                'choices': [
                    ('User interface designs for small applications.', False),
                    ('The architecture of individual programs and their decomposition into components.', True),
                    ('Hardware configurations for large-scale systems.', False),
                    ('Complex enterprise systems distributed over multiple computers.', False),
                ],
                'feedback': '\'Architecture in the small\' refers to the architecture of individual programs and their decomposition into components.'
            },
            {
                'text': 'In Extreme Programming (XP), how frequently are increments typically delivered to customers?',
                'choices': [
                    ('Once every six months', False),
                    ('Several times per day', False),
                    ('Every two weeks', True),
                    ('Twice per year', False),
                ],
                'feedback': 'XP is characterized by a high frequency of delivery to the customer.'
            },
            {
                'text': 'What is the key difference between a system context model and an interaction model?',
                'choices': [
                    ('A context model is dynamic, while an interaction model is structural.', False),
                    ('A context model is structural (showing other systems), while an interaction model is dynamic (showing how the system interacts with its environment).', True),
                    ('A context model shows internal object classes, while an interaction model shows database schemas.', False),
                    ('There is no difference; they are two names for the same model.', False),
                ],
                'feedback': 'A system context model is a structural model that shows the other systems in the environment. An interaction model is a dynamic model that shows how the system interacts with its environment as it is used.'
            },
            {
                'text': 'Software that controls and manages hardware devices (e.g., in appliances or vehicles) is best classified as:',
                'choices': [
                    ('Embedded control systems', True),
                    ('Batch processing systems', False),
                    ('Entertainment systems', False),
                    ('Interactive transaction systems', False),
                ],
                'feedback': 'Embedded control systems are tightly coupled to hardware behavior.'
            },
            {
                'text': 'A defining characteristic of the agile development approach is that it often involves:',
                'choices': [
                    ('Producing a complete and stable set of requirements before any coding begins', False),
                    ('Strict adherence to a detailed, pre-planned sequence of separate development stages', False),
                    ('A single, monolithic deployment at the end of the project life cycle', False),
                    ('The frequent delivery of new software versions or increments', True),
                ],
                'feedback': 'Agile development involves frequent delivery of new versions or increments for evaluation by stakeholders.'
            },
            {
                'text': 'What is identified as perhaps the largest single cause of system failures in sociotechnical systems?',
                'choices': [
                    ('Environmental factors', False),
                    ('Human operator mistakes', True),
                    ('Hardware design errors', False),
                    ('Software implementation bugs', False),
                ],
                'feedback': 'Human operator mistakes are identified as perhaps the largest single cause of system failures in sociotechnical systems.'
            },
            {
                'text': 'How can a non-functional requirement such as a strict response-time constraint influence the project?',
                'choices': [
                    ('It can affect architectural choices, hardware provisioning, and may generate additional functional or design constraints to meet the quality target.', True),
                    ('They are expressed only as absolute equations and have no role in design.', False),
                    ('Non-functional requirements never affect architecture and can be deferred until after implementation.', False),
                    ('They always only concern the user-interface look-and-feel and nothing else.', False),
                ],
                'feedback': 'A non-functional requirement such as a strict response-time constraint can affect architectural choices, hardware provisioning, and may generate additional functional or design constraints to meet the quality target.'
            },
            {
                'text': 'What is the main advantage of applying ethnographic observation when analysing user work practices?',
                'choices': [
                    ('It removes the need for validation and testing later in the project.', False),
                    ('It is useful only for laboratory experiments and not for business systems.', False),
                    ('It uncovers actual practices, informal workarounds and organisational or social issues that stakeholders might not mention in interviews.', True),
                    ('It guarantees the final system will require no future changes.', False),
                ],
                'feedback': 'Ethnographic observation uncovers actual practices, informal workarounds and organisational or social issues that stakeholders might not mention in interviews.'
            },
            {
                'text': 'How can generic application architectures be utilized in software development?',
                'choices': [
                    ('Only for final implementation coding.', False),
                    ('Exclusively for hardware selection.', False),
                    ('To replace detailed requirements analysis.', False),
                    ('As a starting point for architectural design and as a design checklist.', True),
                ],
                'feedback': 'Generic application architectures can be utilized as a starting point for architectural design and as a design checklist.'
            },
            {
                'text': 'Which statement about software costs over a system\'s lifetime is generally true?',
                'choices': [
                    ('Maintenance costs often exceed development costs for long-lived systems', True),
                    ('Hardware costs usually dwarf software costs', False),
                    ('Development always costs more than maintenance', False),
                    ('Costs are evenly split across phases', False),
                ],
                'feedback': 'Maintenance costs often exceed development costs for long-lived systems.'
            },
        ]

        self._load_questions(session, questions)

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] All Midterm questions loaded successfully!'))
        self.stdout.write(f'Total questions in Midterm: {session.questions.count()}')

    def _load_questions(self, session, questions_data):
        """Helper method to load questions into a session"""
        existing_count = session.questions.count()
        created_count = 0
        skipped_count = 0
        
        for idx, q_data in enumerate(questions_data, start=1):
            question, created = Question.objects.get_or_create(
                session=session,
                order=existing_count + idx,
                defaults={
                    'text': q_data['text'],
                    'is_active': True
                }
            )
            
            if created:
                # Create choices for this question
                for choice_text, is_correct in q_data['choices']:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
                created_count += 1
                self.stdout.write(f'  [+] Created question {idx}: {question.text[:50]}...')
            else:
                skipped_count += 1
                self.stdout.write(f'  [-] Question {idx} already exists, skipping: {question.text[:50]}...')
        
        self.stdout.write(f'\nSummary: Created {created_count} questions, skipped {skipped_count} existing questions.')

