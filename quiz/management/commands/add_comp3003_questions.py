from django.core.management.base import BaseCommand
from django.db.models import Max
from quiz.models import Course, Session, Question, Choice
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Adds questions for COMP3003 from HTML file'

    def handle(self, *args, **options):
        # Create or get course
        course, created = Course.objects.get_or_create(
            slug='comp3003',
            defaults={'title': 'COMP3003'}
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
                'text': 'Which statement best describesapplication reuse?',
                'choices': [
                    ('Only reusing databases across unrelated applications.', False),
                    ('Reusing an application by incorporating it without change, or by developing an application family.', True),
                    ('Only reusing APIs while rewriting the entire application implementation.', False),
                    ('Reusing only user interface widgets.', False),
                ]
            },
            {
                'text': 'Reused software is often considered more dependable primarily because:',
                'choices': [
                    ('It has been tried and tested in working systems, so many faults may already have been found and fixed.', True),
                    ('It is always written using formal verification methods.', False),
                    ('It guarantees perfect compatibility with all platforms.', False),
                    ('It avoids the need for any validation testing.', False),
                ]
            },
            {
                'text': 'Why can software reuse reduceprocess riskin project management?',
                'choices': [
                    ('Because reuse always guarantees shorter schedules regardless of integration complexity.', False),
                    ('Because the costs and effort for existing software are already known more reliably than new development.', True),
                    ('Because reused software never contains defects.', False),
                    ('Because reuse eliminates the need for requirements engineering.', False),
                ]
            },
            {
                'text': 'What is the primary purpose of configuration management (CM) in software engineering?',
                'choices': [
                    ('To automatically generate user requirements from code', False),
                    ('To replace all testing with compilation checks', False),
                    ('To eliminate the need for documentation', False),
                    ('To manage and control changes to software artifacts so versions can be tracked and reproduced', True),
                ]
            },
            {
                'text': 'Which set best represents the core activities commonly associated with configuration management?',
                'choices': [
                    ('Version management, system building, change management, and release management', True),
                    ('Data labeling, model training, inference, and hyperparameter tuning', False),
                    ('Incident response, forensics, threat hunting, and patching', False),
                    ('Brainstorming, prototyping, deployment, and marketing', False),
                ]
            },
            {
                'text': 'In a team project, why is configuration management especially important?',
                'choices': [
                    ('It guarantees that all developers write identical code', False),
                    ('It removes the need for code reviews', False),
                    ('It ensures no bugs will be introduced', False),
                    ('It helps prevent conflicting changes and loss of track of what versions are included in a system', True),
                ]
            },
            {
                'text': 'Which description best matches the termbaseline?',
                'choices': [
                    ('A compression technique for storing files', False),
                    ('A temporary scratch area where developers experiment', False),
                    ('A controlled set of component versions that define a specific system version and can be recreated', True),
                    ('A list of all bugs reported by customers', False),
                ]
            },
            {
                'text': 'What is acodelinein version management?',
                'choices': [
                    ('A rule that prevents any change after testing begins', False),
                    ('A customer-facing document describing release notes', False),
                    ('A sequence of versions of a component (and its dependencies) where later versions are derived from earlier ones', True),
                    ('A binary produced after linking object files', False),
                ]
            },
            {
                'text': 'Why isbranchingused in version control?',
                'choices': [
                    ('To encrypt source code before building', False),
                    ('To permanently delete obsolete versions', False),
                    ('To convert source code into object code', False),
                    ('To create an independent line of development so changes can proceed without affecting another line', True),
                ]
            },
            {
                'text': 'What is the main goal ofmergingin version control?',
                'choices': [
                    ('To replace unit tests with manual testing', False),
                    ('To combine changes from different codelines into a new version that includes both sets of modifications', True),
                    ('To revert a repository to its initial state', False),
                    ('To force all developers to use the same editor', False),
                ]
            },
            {
                'text': 'Which statement correctly contrasts centralized and distributed version control systems?',
                'choices': [
                    ('Centralized VC stores no history; distributed VC stores only the latest version', False),
                    ('Centralized VC forbids branching; distributed VC forbids merging', False),
                    ('Centralized VC works only offline; distributed VC requires constant network access', False),
                    ('Centralized VC has a single master repository; distributed VC allows multiple full repository copies to exist concurrently', True),
                ]
            },
            {
                'text': 'What is the main purpose of a privateworkspacein version control?',
                'choices': [
                    ('To store only compiled binaries and forbid source changes', False),
                    ('To serve as the only location where releases are distributed', False),
                    ('To automatically approve customer change requests', False),
                    ('To allow developers to modify files without immediately affecting others or the shared repository', True),
                ]
            },
            {
                'text': 'In practice, what doescloninga repository most closely imply?',
                'choices': [
                    ('Converting all text files into binary format', False),
                    ('Creating a complete local copy of a repository so work can proceed with full history and offline commits', True),
                    ('Locking a single file so nobody else can edit it', False),
                    ('Automatically merging all branches into one', False),
                ]
            },
            {
                'text': 'In a distributed workflow, what is the best interpretation of the difference betweencommitandpush?',
                'choices': [
                    ('A commit records changes in a local repository; a push transfers committed changes to a shared (remote) repository', True),
                    ('A commit is only for binaries; a push is only for source code', False),
                    ('They are identical operations with different names', False),
                    ('A push records changes locally; a commit transfers changes to the remote repository', False),
                ]
            },
            {
                'text': 'Which is a typical benefit of distributed version control compared to purely centralized approaches?',
                'choices': [
                    ('It guarantees smaller repositories than centralized systems', False),
                    ('It prevents any possibility of merge conflicts', False),
                    ('Local repositories enable offline work and provide a natural backup if the server repository is corrupted', True),
                    ('It removes the need for branching and merging', False),
                ]
            },
            {
                'text': 'Historically, why did many version control systems storedeltas(differences) rather than full copies of every version?',
                'choices': [
                    ('To prevent developers from reverting changes', False),
                    ('To avoid the need for unique version identifiers', False),
                    ('To ensure builds always run slower but more accurately', False),
                    ('To reduce disk usage by reconstructing versions from a base version plus stored differences', True),
                ]
            },
            {
                'text': 'Some modern systems prefer storing compressed objects rather than relying on long delta chains. What is a key advantage of that approach?',
                'choices': [
                    ('It prevents branching by design', False),
                    ('It eliminates the need to store any metadata', False),
                    ('Retrieval can be faster because it may only require decompression rather than applying many deltas', True),
                    ('It guarantees that two different files will have the same stored representation', False),
                ]
            },
            {
                'text': 'What best describessystem building?',
                'choices': [
                    ('Converting manual tests into automated tests only', False),
                    ('Collecting user feedback and translating it into requirements', False),
                    ('Encrypting a repository to enforce access control', False),
                    ('Assembling, compiling, and linking the correct components, libraries, and configuration to create an executable system', True),
                ]
            },
            {
                'text': 'Build tools often aim to minimize recompilation. What is the main idea behind this optimization?',
                'choices': [
                    ('Disable linking so builds finish faster', False),
                    ('Compile source files in random order to improve performance', False),
                    ('Recompile only components whose sources have changed compared to the corresponding compiled outputs', True),
                    ('Always rebuild everything to avoid tracking changes', False),
                ]
            },
            {
                'text': 'Which statement is most accurate about using timestamps vs checksums as file signatures in build systems?',
                'choices': [
                    ('Using checksums makes it impossible to rebuild older versions', False),
                    ('Checksums cannot detect a one-character change in source code', False),
                    ('Checksums reflect content changes directly, while timestamps reflect modification times and can be less robust for parallel version builds', True),
                    ('Timestamps change only when the file content changes, never for other reasons', False),
                ]
            },
            {
                'text': 'What is a major benefit of continuous integration (CI)?',
                'choices': [
                    ('CI eliminates all merge conflicts by preventing branching', False),
                    ('CI replaces the need for any version control', False),
                    ('CI guarantees that builds never fail', False),
                    ('Integration problems are detected and fixed early by frequent builds and automated tests', True),
                ]
            },
            {
                'text': 'Which situation is a common challenge (or limitation) when applying continuous integration?',
                'choices': [
                    ('Very large systems may take a long time to build and test, slowing feedback', True),
                    ('CI can be used only for embedded systems', False),
                    ('CI only works if developers never work in parallel', False),
                    ('CI requires banning automated tests', False),
                ]
            },
            {
                'text': 'What is the main objective of change management in software evolution?',
                'choices': [
                    ('To avoid documenting changes to reduce paperwork', False),
                    ('To assess, approve, prioritize, and track changes so evolution is controlled and cost-effective', True),
                    ('To ensure every requested change is implemented immediately', False),
                    ('To prevent any changes after initial deployment', False),
                ]
            },
            {
                'text': 'Which option best lists factors commonly considered during change analysis?',
                'choices': [
                    ('Only the number of lines of code in the system', False),
                    ('Only marketing slogans and UI color themes', False),
                    ('Only the programming language used and code style rules', False),
                    ('Consequences of not changing, benefits, users affected, cost of change, and release cycle considerations', True),
                ]
            },
            {
                'text': 'What is a typical role of a change control board (CCB) or equivalent authority?',
                'choices': [
                    ('To prevent any bug fixes during system testing', False),
                    ('To rename branches according to a naming convention', False),
                    ('To decide which change requests are accepted and when they should be implemented', True),
                    ('To compile the software and produce executables', False),
                ]
            },
            {
                'text': 'Which statement best distinguishes major and minor releases?',
                'choices': [
                    ('Major releases are internal only, minor releases are customer-facing only', False),
                    ('Minor releases must introduce new modules, major releases must not', False),
                    ('Major releases deliver significant new functionality, while minor releases typically focus on bug fixes and small improvements', True),
                    ('There is no difference; the terms are interchangeable', False),
                ]
            },
            {
                'text': 'Beyond executable code, what may a software release commonly include?',
                'choices': [
                    ('Only marketing videos and branding assets', False),
                    ('Only unit test source files', False),
                    ('Configuration files, data files (e.g., messages), installation scripts/programs, and documentation', True),
                    ('Only the source code, never any configuration or data', False),
                ]
            },
            {
                'text': 'Which factor can legitimately force an organization to plan a new software release?',
                'choices': [
                    ('The absence of any reported defects for many years', False),
                    ('A platform change such as a new operating system version that requires compatibility updates', True),
                    ('A rule that releases must occur only once per decade', False),
                    ('The desire to avoid keeping any release records', False),
                ]
            },
            {
                'text': 'Why is documenting a release so that it can be recreated exactly later considered important?',
                'choices': [
                    ('To reproduce the exact delivered software when diagnosing issues, especially for long-lived or customized deployments', True),
                    ('To ensure old releases cannot be rebuilt for security reasons', False),
                    ('To force customers to upgrade to the newest release immediately', False),
                    ('To avoid using version identifiers likeV1.2', False),
                ]
            },
            {
                'text': 'Which information is most critical to record to enable faithful release reproduction?',
                'choices': [
                    ('Only a list of programming languages used', False),
                    ('Exact component versions, executables, configuration/data files, and build environment versions (OS, libraries, compiler/tools)', True),
                    ('Only the project logo and marketing tagline', False),
                    ("Only developers' personal workstation settings", False),
                ]
            },
            {
                'text': 'Which option best matches the typical roles of development system, build server, and target environment?',
                'choices': [
                    ('Developers edit locally; the build server produces definitive executables; the target environment is where the system runs', True),
                    ('The target environment compiles code; developers deploy tools; the build server writes requirements', False),
                    ('The build server is used only for UI design and user interviews', False),
                    ('Only the target environment stores versions; developers do not use repositories', False),
                ]
            },
            {
                'text': 'Which statement best reflects the idea of a daily build process?',
                'choices': [
                    ('Developers must avoid committing changes until the end of the month', False),
                    ('Only documentation is updated daily; code is never rebuilt', False),
                    ('Components are delivered by a cutoff time, integrated into a system build, and then tested using predefined system tests', True),
                    ('Daily builds require removing automated tests to save time', False),
                ]
            },
            {
                'text': 'How does delivering software as a service (SaaS) typically affect release management?',
                'choices': [
                    ('It requires customers to build executables themselves', False),
                    ('It guarantees no release documentation is needed', False),
                    ('It eliminates the need for version management entirely', False),
                    ('It can simplify distribution and installation because the provider deploys updates centrally for all customers', True),
                ]
            },
            {
                'text': 'Which statement best distinguishesdesign-time configurationfromdeployment-time configuration?',
                'choices': [
                    ('They are identical terms used interchangeably in software reuse.', False),
                    ('Deployment-time configuration requires recompiling the system for every change.', False),
                    ('Design-time configuration is performed by the developing organization to create a new system; deployment-time configuration is performed by customers/consultants using embedded configuration data.', True),
                    ('Design-time configuration happens after installation; deployment-time configuration happens before coding.', False),
                ]
            },
            {
                'text': 'What is a primary goal of an Enterprise Resource Planning (ERP) system?',
                'choices': [
                    ('To provide a generic system supporting common business processes (e.g., ordering, invoicing, manufacturing) that can be configured for an organization.', True),
                    ('To generate code from models usingθandαparameters.', False),
                    ('To act only as a document editor for office files.', False),
                    ('To replace all business processes with a single fixed workflow that cannot be changed.', False),
                ]
            },
            {
                'text': 'Which activity is a typical way to extend an application framework?',
                'choices': [
                    ('Adding concrete classes that inherit from abstract classes and implementing event-handling methods (callbacks).', True),
                    ('Deleting all abstract classes and keeping only utilities.', False),
                    ('Replacing the entire framework core to remove abstraction.', False),
                    ('Disabling event loops so the framework never invokes user code.', False),
                ]
            },
            {
                'text': 'Which option is an example of asystem infrastructure framework?',
                'choices': [
                    ('A framework that only provides domain rules for insurance pricing.', False),
                    ('A spreadsheet template used for budgeting.', False),
                    ('A framework supporting development of infrastructure such as communications or user interfaces.', True),
                    ('A framework that only supplies test data generators.', False),
                ]
            },
            {
                'text': 'Which description best matches anapplication framework?',
                'choices': [
                    ('An integrated set of software artifacts that collaborate to provide a reusable architecture for a family of related applications.', True),
                    ('A hardware platform used to deploy software systems.', False),
                    ('A database schema that stores application data.', False),
                    ('A single function that can be copied and pasted into any program.', False),
                ]
            },
            {
                'text': 'In many frameworks,inversion of controlmeans that:',
                'choices': [
                    ('The framework controls the flow and calls application-specific code via events and callbacks.', True),
                    ('Callbacks are replaced by polling loops written by the application.', False),
                    ('All code must be written in a functional programming style.', False),
                    ('The application must never depend on any external libraries.', False),
                ]
            },
            {
                'text': 'In the Model-View-Controller (MVC) pattern, what is a typical responsibility of theController?',
                'choices': [
                    ('Compiling source code into machine code.', False),
                    ('Handling user inputs and translating them into actions that update the model and/or the view.', True),
                    ('Rendering every user interface element directly with no separation.', False),
                    ('Storing all persistent data and enforcing database transactions.', False),
                ]
            },
            {
                'text': 'Which statement best describessoftware project management?',
                'choices': [
                    ('Ensuring software is delivered on time, within budget, and aligned with agreed requirements', True),
                    ('Writing source code as quickly as possible to maximize developer productivity', False),
                    ('Replacing all planning with ad-hoc decisions to remain flexible', False),
                    ('Guaranteeing that requirements never change throughout development', False),
                ]
            },
            {
                'text': 'Which option isNOTtypically considered a key success criterion for a software project?',
                'choices': [
                    ('Delivering the software at the agreed time', False),
                    ('Keeping overall costs within the budget', False),
                    ('Making the team as large as possible to cover every possible task', True),
                    ('Maintaining a coherent and well-functioning development team', False),
                ]
            },
            {
                'text': 'Why is software project management often considered distinct from managing physical engineering projects?',
                'choices': [
                    ('Software requirements are always fully defined and stable at project start', False),
                    ("Software is intangible and progress is harder to 'see' directly compared to physical artifacts", True),
                    ('Software always uses identical processes regardless of the organization', False),
                    ('Software projects never have budget or schedule constraints', False),
                ]
            },
            {
                'text': 'Which activity is most closely associated withrisk managementin software projects?',
                'choices': [
                    ('Identifying potential threats to the project and preparing actions to reduce their impact', True),
                    ('Avoiding any reporting to stakeholders to reduce pressure on the team', False),
                    ('Choosing a programming language solely based on developer preference', False),
                    ('Refusing to change project plans under any circumstances', False),
                ]
            },
            {
                'text': 'A risk that primarily threatensscheduleorresourcesis best classified as which of the following?',
                'choices': [
                    ('Compliance risk only', False),
                    ('Product risk', False),
                    ('Project risk', True),
                    ('Business risk', False),
                ]
            },
            {
                'text': 'Which situation is the best example of aproduct risk?',
                'choices': [
                    ('Senior management changes priorities and reduces staffing allocation', False),
                    ('Key engineers leave the team, forcing a schedule slip', False),
                    ('A critical development tool performs far worse than expected, reducing output quality', True),
                    ('A competitor launches a similar product first, harming market position', False),
                ]
            },
            {
                'text': 'Which sequence best matches a standard risk management workflow?',
                'choices': [
                    ('Risk analysis → Risk identification → Risk planning → Risk monitoring', False),
                    ('Risk planning → Risk identification → Risk monitoring → Risk analysis', False),
                    ('Risk identification → Risk analysis → Risk planning → Risk monitoring', True),
                    ('Risk monitoring → Risk planning → Risk analysis → Risk identification', False),
                ]
            },
            {
                'text': 'In risk analysis, what is typically assessed for each risk?',
                'choices': [
                    ('Only the financial cost if the risk happens, ignoring schedule effects', False),
                    ('The personal preferences of the project manager', False),
                    ('The probability of occurrence and the seriousness of its consequences', True),
                    ('Only technical feasibility, ignoring organizational conditions', False),
                ]
            },
            {
                'text': 'Which set best represents common qualitative categories used for risk likelihood?',
                'choices': [
                    ('New, used, refurbished, legacy, obsolete', False),
                    ('Alpha, beta, gamma, delta, theta', False),
                    ('Very low, low, moderate, high, very high', True),
                    ('Bronze, silver, gold, platinum, diamond', False),
                ]
            },
            {
                'text': 'Which option is most consistent with common qualitative categories for risk consequences?',
                'choices': [
                    ('Catastrophic, serious, tolerable, insignificant', True),
                    ('Cheap, affordable, expensive, priceless', False),
                    ('Green, yellow, orange, purple', False),
                    ('Fast, medium, slow, frozen', False),
                ]
            },
            {
                'text': 'Which choice correctly matches a typical set of risk response strategies?',
                'choices': [
                    ('Only avoidance, because planning for failure is unacceptable', False),
                    ('Only contingency plans, because likelihood cannot be influenced', False),
                    ('Denial, blame shifting, and ignoring warning signs', False),
                    ('Avoidance, minimization, contingency plans', True),
                ]
            },
            {
                'text': "In risk planning, what is the main purpose of asking 'what-if' questions?",
                'choices': [
                    ('To explore scenarios so avoidance and contingency actions can be prepared in advance', True),
                    ('To prove that risks are impossible and can be ignored', False),
                    ('To replace monitoring with a single meeting at project start', False),
                    ('To assign fault in advance to one person if problems happen', False),
                ]
            },
            {
                'text': 'Which best describesrisk monitoringduring a software project?',
                'choices': [
                    ('Regularly reassessing identified risks and discussing key risks in progress meetings', True),
                    ('Documenting risks once and never revisiting them', False),
                    ('Eliminating all uncertainty by removing stakeholder input', False),
                    ('Treating every risk as equally urgent regardless of probability or impact', False),
                ]
            },
            {
                'text': 'Which is a common indicator ofestimation-relatedproject risk?',
                'choices': [
                    ('Failure to meet the agreed schedule and failure to clear reported defects', True),
                    ('Late delivery of essential hardware', False),
                    ('Organizational gossip about restructuring', False),
                    ('Many requests for higher-powered workstations', False),
                ]
            },
            {
                'text': "A manager ensures all team members' views are considered and everyone is involved in decisions that affect their work. Which people management factor does this best represent?",
                'choices': [
                    ('Inclusion', True),
                    ('Secrecy', False),
                    ('Micromanagement', False),
                    ('Favouritism', False),
                ]
            },
            {
                'text': 'In a project setting, what doesmotivating peopleprimarily mean?',
                'choices': [
                    ('Increasing meeting frequency until productivity improves automatically', False),
                    ('Assuming motivation is fixed and cannot change over time', False),
                    ('Organizing work and the environment to encourage effective and engaged performance', True),
                    ('Avoiding feedback to prevent conflict', False),
                ]
            },
            {
                'text': 'Which action best supportsesteemneeds in a professional software team?',
                'choices': [
                    ('Forbidding informal communication to prevent distractions', False),
                    ('Recognizing achievements and providing appropriate rewards', True),
                    ('Eliminating training because it does not produce immediate code', False),
                    ('Removing autonomy so that everyone follows identical scripts', False),
                ]
            },
            {
                'text': 'Which description best matches aninteraction-orientedpersonality type in a software team?',
                'choices': [
                    ('Someone motivated only by personal recognition and promotion outcomes', False),
                    ('Someone motivated mainly by working with others and being part of the group', True),
                    ('Someone motivated exclusively by the technical challenge of the task itself', False),
                    ('Someone who refuses all collaboration because team work is always harmful', False),
                ]
            },
            {
                'text': 'Why can a team composed entirely of people with thesamemotivation style be problematic?',
                'choices': [
                    ('It can amplify a single weakness (e.g., everyone wants to lead, or too much discussion and not enough execution)', True),
                    ('It removes the need for communication, since agreement is automatic', False),
                    ('It eliminates all project risks by simplifying management', False),
                    ('It guarantees the highest productivity because everyone thinks the same way', False),
                ]
            },
            {
                'text': 'Why is software engineering commonly agroup activityfor non-trivial systems?',
                'choices': [
                    ('Individual developers cannot learn new technologies', False),
                    ('The schedule and complexity generally require multiple people with diverse skills to meet goals', True),
                    ('Regulations forbid individuals from developing software alone', False),
                    ('Teams always write less code than individuals, which reduces defects', False),
                ]
            },
            {
                'text': 'What best characterizes acohesiveproject group?',
                'choices': [
                    ("Members work independently and never review each other's work", False),
                    ('Members avoid sharing knowledge to protect personal advantage', False),
                    ('Members focus only on individual metrics, ignoring team outcomes', False),
                    ('Members consider the group and its goals more important than individual preference', True),
                ]
            },
            {
                'text': 'Which benefit is most associated with a cohesive software development group?',
                'choices': [
                    ('Knowledge is shared so continuity is maintained even if a member leaves', True),
                    ('Refactoring is avoided because only the original author may change code', False),
                    ('Testing becomes unnecessary because group spirit replaces verification', False),
                    ('Bugs are impossible because cohesive teams never make mistakes', False),
                ]
            },
            {
                'text': 'Which set best captures key factors that influence the effectiveness of a software team?',
                'choices': [
                    ('Office paint color, brand of laptops, and number of elevators in the building', False),
                    ('Only the programming language and the version control system', False),
                    ("Only the project manager's individual technical skill", False),
                    ('People in the group, group organization, and technical/managerial communications', True),
                ]
            },
            {
                'text': 'Which is a typicalgroup organizationquestion a project must decide early?',
                'choices': [
                    ('Whether documentation should be banned entirely', False),
                    ('Which developer should be excluded from all meetings to improve speed?', False),
                    ('Who will be involved in making critical technical decisions, and how will these be made?', True),
                    ('What is the only acceptable keyboard layout for the team?', False),
                ]
            },
            {
                'text': 'Which description best matches aninformalsoftware engineering group structure?',
                'choices': [
                    ('The team discusses work collectively and allocates tasks based on ability and experience, with the leader serving as an external interface', True),
                    ('Separate sub-groups report through multiple management layers for every minor decision', False),
                    ('Decisions are made by random selection to avoid conflict', False),
                    ('The leader assigns every task unilaterally without discussion', False),
                ]
            },
            {
                'text': 'An informal group structure is most likely to succeed when:',
                'choices': [
                    ('No one knows the domain, but the deadline is tomorrow', False),
                    ('The team is forced to avoid communication to save time', False),
                    ('All members are experienced and competent enough to coordinate and decide collectively', True),
                    ('Stakeholders prohibit the team from making any decisions', False),
                ]
            },
            {
                'text': 'What is a typical effect of increasing group size on communication?',
                'choices': [
                    ('Communication becomes irrelevant because tasks can be fully isolated', False),
                    ('Communication always becomes perfect because there are more people to talk', False),
                    ('Communication generally becomes harder as the group gets larger', True),
                    ('Communication improves automatically even without processes or tools', False),
                ]
            },
            {
                'text': 'Compared with hierarchical groups, communication is typically better in:',
                'choices': [
                    ('Informally structured groups', True),
                    ('Groups where members are discouraged from sharing status updates', False),
                    ('Groups where design decisions are never discussed', False),
                    ('Groups where all communication must go through one executive', False),
                ]
            },
            {
                'text': 'Which team composition is most likely to support healthier communication?',
                'choices': [
                    ('A team with varied personality types where members complement each other', True),
                    ('A team that bans informal conversation entirely', False),
                    ('A team where only one person is allowed to speak during discussions', False),
                    ('A team where everyone has identical motivations and avoids disagreement at all costs', False),
                ]
            },
            {
                'text': 'When dealing with frequent requirements change requests, which practice best helps assess the impact of changes?',
                'choices': [
                    ('Maintaining requirements traceability to analyze downstream impact', True),
                    ('Accepting every change immediately without impact analysis', False),
                    ('Measuring impact by counting how many meetings were held about the change', False),
                    ('Refusing all change requests after the first week', False),
                ]
            },
            {
                'text': 'Which challenge is most directly associated with creating and using a reusable component library?',
                'choices': [
                    ('It can be expensive to populate, maintain, and adapt development processes so developers actually use it.', True),
                    ('It eliminates the need for version control in development teams.', False),
                    ('It guarantees that all components are interchangeable without changes.', False),
                    ('It removes the need for documentation entirely.', False),
                ]
            },
            {
                'text': "What does the'not-invented-here'syndrome describe?",
                'choices': [
                    ('A preference to rewrite components rather than reuse them, often due to trust or perceived challenge.', True),
                    ('A policy requiring all software to be developed in-house for legal reasons.', False),
                    ('A technique to automatically generate software from models.', False),
                    ('A strategy where teams only reuse open-source code.', False),
                ]
            },
            {
                'text': 'When producing a new member of a software product line, which step most directly involves selecting an existing family member that best matches requirements?',
                'choices': [
                    ('Reverse engineer the database schema.', False),
                    ('Set up continuous integration pipelines.', False),
                    ('Choose closest-fit family member (system instance).', True),
                    ('Deliver new family member.', False),
                ]
            },
            {
                'text': 'In a typical product line base system, which category is least likely to be modified when creating a new family member?',
                'choices': [
                    ('Customer-specific plug-ins implemented for unique requirements.', False),
                    ('Specialized domain-specific components that may be replaced for new instances.', False),
                    ('Core components that provide infrastructure support.', True),
                    ('Configurable components that are adjusted to specialize for a customer.', False),
                ]
            },
            {
                'text': 'Creating different versions of an application to run on different operating systems is an example of:',
                'choices': [
                    ('Process specialization.', False),
                    ('Functional specialization.', False),
                    ('Platform specialization.', True),
                    ('Environment specialization.', False),
                ]
            },
            {
                'text': 'In reuse-based development, the termreuse landscapeprimarily refers to:',
                'choices': [
                    ('A security model describing trust zones for third-party components.', False),
                    ('A list of programming languages that support code reuse.', False),
                    ('A geographic map of where software libraries are hosted.', False),
                    ('The range of reuse techniques available, from small functions to complete application systems.', True),
                ]
            },
            {
                'text': 'Which of the following is a key factor to consider when planning a reuse strategy?',
                'choices': [
                    ('The expected lifetime of the software and how long it must be maintained.', True),
                    ('Whether the team uses tabs or spaces in code formatting.', False),
                    ('The preferred font size for documentation.', False),
                    ('The number of colors used in the user interface theme.', False),
                ]
            },
            {
                'text': 'Which statement best distinguishes asociotechnicalsystem from a purelytechnicalcomputer-based system?',
                'choices': [
                    ('It is defined only by having strict real-time constraints and embedded hardware.', False),
                    ('It includes technology as well as people, processes, and organizational policies that shape how the system is used.', True),
                    ('It is any system that runs on a computer, regardless of users or environment.', False),
                    ('It must be composed exclusively of off-the-shelf components.', False),
                ]
            },
            {
                'text': 'Which statement best distinguishes asociotechnicalsystem from a purelytechnicalcomputer-based system?',
                'choices': [
                    ('It includes technology as well as people, processes, and organizational policies that shape how the system is used.', True),
                    ('It is any system that runs on a computer, regardless of users or environment.', False),
                    ('It must be composed exclusively of off-the-shelf components.', False),
                    ('It is defined only by having strict real-time constraints and embedded hardware.', False),
                ]
            },
            {
                'text': 'Which statement best describessecurity engineeringin software development?',
                'choices': [
                    ('It is primarily about maximizing performance by removing authentication checks.', False),
                    ('It applies tools, techniques, and methods to help systems resist malicious attacks that could damage the system or its data.', True),
                    ('It focuses exclusively on making systems user-friendly, even if that weakens protection.', False),
                    ('It only concerns physical security such as locks and surveillance cameras.', False),
                ]
            },
            {
                'text': 'Which activity set is most aligned with systems engineering for large organizational systems?',
                'choices': [
                    ('Writing code modules and unit tests for a single application component.', False),
                    ('Only selecting programming languages and development frameworks.', False),
                    ('Only installing purchased software without changing business processes.', False),
                    ('Procuring, specifying, designing, implementing, validating, deploying, and maintaining a system that includes people and organizational processes.', True),
                ]
            },
            {
                'text': 'Which activity set is most aligned with systems engineering for large organizational systems?',
                'choices': [
                    ('Procuring, specifying, designing, implementing, validating, deploying, and maintaining a system that includes people and organizational processes.', True),
                    ('Writing code modules and unit tests for a single application component.', False),
                    ('Only selecting programming languages and development frameworks.', False),
                    ('Only installing purchased software without changing business processes.', False),
                ]
            },
            {
                'text': 'In the security triad of confidentiality, integrity, and availability, what doesconfidentialityprimarily protect against?',
                'choices': [
                    ('Unauthorized disclosure of information to people or programs that should not access it.', True),
                    ('Accidental deletion of records due to power loss.', False),
                    ('Ensuring data can be modified by any authenticated user.', False),
                    ('Slow response times caused by encryption overhead.', False),
                ]
            },
            {
                'text': 'What is the primary purpose ofconceptual designin a systems engineering process?',
                'choices': [
                    ('To finalize detailed interface specifications for all subsystems before any stakeholder discussion.', False),
                    ('To write the final user manual and training materials.', False),
                    ('To investigate feasibility and create a high-level vision of the system, including why it is needed and what services it should provide.', True),
                    ('To perform only low-level performance tuning after deployment.', False),
                ]
            },
            {
                'text': 'What is the primary purpose ofconceptual designin a systems engineering process?',
                'choices': [
                    ('To write the final user manual and training materials.', False),
                    ('To investigate feasibility and create a high-level vision of the system, including why it is needed and what services it should provide.', True),
                    ('To finalize detailed interface specifications for all subsystems before any stakeholder discussion.', False),
                    ('To perform only low-level performance tuning after deployment.', False),
                ]
            },
            {
                'text': 'What best characterizesintegrityas a security dimension?',
                'choices': [
                    ('Guaranteeing that users can always reach the system during peak demand.', False),
                    ('Preventing information from being damaged or corrupted so it remains reliable and accurate.', True),
                    ('Reducing server costs by removing audit logs.', False),
                    ('Ensuring all data is publicly readable to increase transparency.', False),
                ]
            },
            {
                'text': 'In interdisciplinary system development, which issue most commonly causes misunderstanding across professional disciplines?',
                'choices': [
                    ('Misunderstandings happen only after the system is deployed.', False),
                    ('All disciplines always share identical assumptions about constraints and feasibility.', False),
                    ('Professional boundaries never affect technical decisions.', False),
                    ('Different disciplines may use the same terms to mean different things, leading to mismatched expectations about what will be implemented.', True),
                ]
            },
            {
                'text': 'In interdisciplinary system development, which issue most commonly causes misunderstanding across professional disciplines?',
                'choices': [
                    ('All disciplines always share identical assumptions about constraints and feasibility.', False),
                    ('Misunderstandings happen only after the system is deployed.', False),
                    ('Different disciplines may use the same terms to mean different things, leading to mismatched expectations about what will be implemented.', True),
                    ('Professional boundaries never affect technical decisions.', False),
                ]
            },
            {
                'text': 'Which situation is the best example of anavailabilityproblem?',
                'choices': [
                    ('A user edits a transaction amount without authorization.', False),
                    ('A password policy requires at least 14 characters.', False),
                    ('An attacker reads confidential customer records without changing them.', False),
                    ('A denial of service attack floods a server so legitimate users cannot access the service.', True),
                ]
            },
            {
                'text': 'A layered model of sociotechnical systems places the technical system inside broader layers. Which outer layer is most likely to constrain the systemindirectlythrough organizational decisions?',
                'choices': [
                    ('The choice of sorting algorithm in a utility library.', False),
                    ('Organizational policies and rules.', True),
                    ('The voltage rating of a circuit resistor.', False),
                    ('The CPU cache hierarchy.', False),
                ]
            },
            {
                'text': 'A layered model of sociotechnical systems places the technical system inside broader layers. Which outer layer is most likely to constrain the systemindirectlythrough organizational decisions?',
                'choices': [
                    ('The choice of sorting algorithm in a utility library.', False),
                    ('The voltage rating of a circuit resistor.', False),
                    ('Organizational policies and rules.', True),
                    ('The CPU cache hierarchy.', False),
                ]
            },
            {
                'text': 'Which option best distinguishesapplication securityfrominfrastructure security?',
                'choices': [
                    ('Application security is about physical access; infrastructure security is about cryptography only.', False),
                    ('Application security only concerns firewalls; infrastructure security only concerns code reviews.', False),
                    ('They are identical terms and used interchangeably in engineering practice.', False),
                    ('Application security is primarily a software engineering/design problem; infrastructure security is primarily a systems configuration/management problem.', True),
                ]
            },
            {
                'text': 'Which scenario best illustrates why organizational context matters for system acceptance?',
                'choices': [
                    ('A new system forces major process changes and threatens job roles, so users resist despite correct functionality.', True),
                    ('An API changes a parameter name but all clients are updated automatically.', False),
                    ('A compiler emits faster machine code after an optimization pass.', False),
                    ('The system uses a newer database version with fewer features.', False),
                ]
            },
            {
                'text': 'Which scenario best illustrates why organizational context matters for system acceptance?',
                'choices': [
                    ('An API changes a parameter name but all clients are updated automatically.', False),
                    ('The system uses a newer database version with fewer features.', False),
                    ('A compiler emits faster machine code after an optimization pass.', False),
                    ('A new system forces major process changes and threatens job roles, so users resist despite correct functionality.', True),
                ]
            },
            {
                'text': 'Why isoperational securityoften described as primarily a human and social issue?',
                'choices': [
                    ('Because users may take convenient but insecure actions, creating a trade-off between security and getting work done effectively.', True),
                    ('Because operational security is unrelated to policy and procedures.', False),
                    ('Because operational security only involves selecting a programming language.', False),
                    ('Because operational security can be solved completely by adding more encryption.', False),
                ]
            },
            {
                'text': 'Which statement best describes anemergent propertyof a system?',
                'choices': [
                    ('A property that can always be computed as the sum of individual component properties.', False),
                    ('A requirement that is always written explicitly in the contract.', False),
                    ('A system-level characteristic that arises from interactions among components and may only be evaluated after integration.', True),
                    ('A feature that exists only in software, never in hardware systems.', False),
                ]
            },
            {
                'text': 'Which statement best describes anemergent propertyof a system?',
                'choices': [
                    ('A requirement that is always written explicitly in the contract.', False),
                    ('A system-level characteristic that arises from interactions among components and may only be evaluated after integration.', True),
                    ('A feature that exists only in software, never in hardware systems.', False),
                    ('A property that can always be computed as the sum of individual component properties.', False),
                ]
            },
            {
                'text': 'In security engineering, what is anasset?',
                'choices': [
                    ('Any bug found during unit testing.', False),
                    ('Only cryptographic keys and passwords.', False),
                    ('A public document that everyone can freely access.', False),
                    ('Something of value that has to be protected, such as a system component or data.', True),
                ]
            },
            {
                'text': 'Which option is an example of anon-functional emergentproperty in a deployed operational environment?',
                'choices': [
                    ("The system can print an invoice after clicking 'Generate'.", False),
                    ('Reliability of the overall system when components and operators interact.', True),
                    ('The system can store a record in a database table.', False),
                    ("The system includes a 'Help' menu item.", False),
                ]
            },
            {
                'text': 'Which option is an example of anon-functional emergentproperty in a deployed operational environment?',
                'choices': [
                    ('Reliability of the overall system when components and operators interact.', True),
                    ("The system includes a 'Help' menu item.", False),
                    ('The system can store a record in a database table.', False),
                    ("The system can print an invoice after clicking 'Generate'.", False),
                ]
            },
            {
                'text': 'What is avulnerabilityin a computer-based system?',
                'choices': [
                    ('A user account that has multi-factor authentication enabled.', False),
                    ('A weakness that may be exploited to cause loss or harm.', True),
                    ('A guarantee that data will remain correct under all conditions.', False),
                    ('A backup copy of a database.', False),
                ]
            },
            {
                'text': 'Let component reliabilities beR1,R2,…,Rn. Why might the overall system reliabilityRsysnotbe accurately predicted by simply combining individual reliabilities?',
                'choices': [
                    ('BecauseRsysalways equalsR1+R2+⋯+Rnby definition.', False),
                    ('Because component testing is illegal in most procurement contracts.', False),
                    ('Because reliability is only a software concept and cannot be applied to systems with hardware.', False),
                    ('Because unforeseen interactions and dependency chains can introduce new failure modes, soRsysreflects more than isolated component behavior.', True),
                ]
            },
            {
                'text': 'Let component reliabilities beR1,R2,…,Rn. Why might the overall system reliabilityRsysnotbe accurately predicted by simply combining individual reliabilities?',
                'choices': [
                    ('Because reliability is only a software concept and cannot be applied to systems with hardware.', False),
                    ('Because component testing is illegal in most procurement contracts.', False),
                    ('BecauseRsysalways equalsR1+R2+⋯+Rnby definition.', False),
                    ('Because unforeseen interactions and dependency chains can introduce new failure modes, soRsysreflects more than isolated component behavior.', True),
                ]
            },
            {
                'text': 'Which statement best explains the relationship between athreatand anattack?',
                'choices': [
                    ('A threat is always accidental; an attack is always unintentional.', False),
                    ('An attack is a protective measure; a threat is the control that reduces vulnerability.', False),
                    ('A threat and an attack mean the same thing in risk analysis.', False),
                    ('A threat is the potential for harm; an attack is an exploitation of a vulnerability that attempts to cause damage.', True),
                ]
            },
            {
                'text': 'Which statement best explainsfailure propagationin complex systems?',
                'choices': [
                    ('A fault in one component can trigger incorrect behavior in dependent components, potentially cascading into a system failure.', True),
                    ('Failures only occur independently, so one failing component cannot affect others.', False),
                    ('Propagation can happen only in hardware, never in software or operations.', False),
                    ('Propagation is prevented automatically by using off-the-shelf components.', False),
                ]
            },
            {
                'text': 'Which statement best explainsfailure propagationin complex systems?',
                'choices': [
                    ('Propagation can happen only in hardware, never in software or operations.', False),
                    ('A fault in one component can trigger incorrect behavior in dependent components, potentially cascading into a system failure.', True),
                    ('Propagation is prevented automatically by using off-the-shelf components.', False),
                    ('Failures only occur independently, so one failing component cannot affect others.', False),
                ]
            },
            {
                'text': 'Which option is the best example of acontrolin security engineering?',
                'choices': [
                    ('Encrypting sensitive files so unauthorized users cannot read them.', True),
                    ("A weak password policy that allows 'password123'.", False),
                    ('Storing secrets in plain text to simplify debugging.', False),
                    ('Removing audit logs to reduce storage costs.', False),
                ]
            },
            {
                'text': 'A deterministic system produces the same outputs for the same inputs. Why can sociotechnical systems be non-deterministic even when the software is deterministic?',
                'choices': [
                    ('Because overall behavior depends partly on human actions and operational context, which may vary even under the same nominal inputs.', True),
                    ('Because procurement decisions automatically randomize system outputs.', False),
                    ('Because deterministic software is impossible to build in practice.', False),
                    ('Because determinism is defined only for mechanical systems, not computer systems.', False),
                ]
            },
            {
                'text': 'A deterministic system produces the same outputs for the same inputs. Why can sociotechnical systems be non-deterministic even when the software is deterministic?',
                'choices': [
                    ('Because procurement decisions automatically randomize system outputs.', False),
                    ('Because determinism is defined only for mechanical systems, not computer systems.', False),
                    ('Because deterministic software is impossible to build in practice.', False),
                    ('Because overall behavior depends partly on human actions and operational context, which may vary even under the same nominal inputs.', True),
                ]
            },
            {
                'text': 'Which scenario best fits aninterceptionthreat type?',
                'choices': [
                    ('An attacker captures network traffic to obtain confidential user data being transferred.', True),
                    ('An attacker deletes database tables to prevent service operation.', False),
                    ('An attacker changes a patient record to an incorrect value.', False),
                    ('An attacker inserts a fake transaction into a banking system.', False),
                ]
            },
            {
                'text': "Complex systems often address 'wicked problems'. What is a key implication for defining system success?",
                'choices': [
                    ('Success may be subjective and depend on stakeholder perspectives and real-world effectiveness after deployment, not just original specifications.', True),
                    ('If a contract is signed, the system is automatically successful.', False),
                    ('Success can always be measured objectively by counting lines of code delivered.', False),
                    ('Wicked problems imply that requirements can be completely specified up front with no ambiguity.', False),
                ]
            },
            {
                'text': "Complex systems often address 'wicked problems'. What is a key implication for defining system success?",
                'choices': [
                    ('If a contract is signed, the system is automatically successful.', False),
                    ('Success can always be measured objectively by counting lines of code delivered.', False),
                    ('Success may be subjective and depend on stakeholder perspectives and real-world effectiveness after deployment, not just original specifications.', True),
                    ('Wicked problems imply that requirements can be completely specified up front with no ambiguity.', False),
                ]
            },
            {
                'text': 'Which scenario is most clearly aninterruptionthreat?',
                'choices': [
                    ('Creating fake user accounts to inflate analytics.', False),
                    ('Overwhelming a web server with requests so legitimate users cannot connect.', True),
                    ('Stealing a file that contains confidential employee salaries.', False),
                    ('Quietly altering a configuration value to weaken access control.', False),
                ]
            },
            {
                'text': 'Which activity best matches a feasibility study in early system design?',
                'choices': [
                    ('Assessing whether a proposed system can be implemented with available hardware/software and learning from similar existing systems.', True),
                    ('Running full system acceptance tests in the customer environment.', False),
                    ('Deploying the system and migrating production data.', False),
                    ('Optimizing database indexes based on production workload measurements.', False),
                ]
            },
            {
                'text': 'Which activity best matches a feasibility study in early system design?',
                'choices': [
                    ('Deploying the system and migrating production data.', False),
                    ('Optimizing database indexes based on production workload measurements.', False),
                    ('Running full system acceptance tests in the customer environment.', False),
                    ('Assessing whether a proposed system can be implemented with available hardware/software and learning from similar existing systems.', True),
                ]
            },
            {
                'text': 'Which option best illustrates amodificationthreat?',
                'choices': [
                    ('An attacker blocks access to a system by flooding it with traffic.', False),
                    ('An attacker changes stored records so the information becomes incorrect or unreliable.', True),
                    ('An attacker adds an entirely new, fake record that never existed.', False),
                    ('An attacker reads a confidential report without changing it.', False),
                ]
            },
            {
                'text': 'Why is a system vision document typically written in a readable, non-technical style?',
                'choices': [
                    ('To hide the technical design from suppliers until procurement ends.', False),
                    ('To communicate the system purpose and proposed services to stakeholders and decision makers who may not be technical specialists.', True),
                    ('So that it can replace all requirements specifications and design documents.', False),
                    ('Because legal contracts forbid technical details.', False),
                ]
            },
            {
                'text': 'Why is a system vision document typically written in a readable, non-technical style?',
                'choices': [
                    ('To communicate the system purpose and proposed services to stakeholders and decision makers who may not be technical specialists.', True),
                    ('To hide the technical design from suppliers until procurement ends.', False),
                    ('So that it can replace all requirements specifications and design documents.', False),
                    ('Because legal contracts forbid technical details.', False),
                ]
            },
            {
                'text': 'Which scenario is the best example of afabricationthreat?',
                'choices': [
                    ('Sniffing network packets to capture a password.', False),
                    ('Blocking system access by taking down a server.', False),
                    ('Injecting a fraudulent transaction into a financial system to transfer funds.', True),
                    ('Overwriting an existing file to corrupt it.', False),
                ]
            },
            {
                'text': 'Which factor is most likely to be a major driver for initiating system procurement in an organization?',
                'choices': [
                    ('Increasing the number of programming languages allowed in the codebase.', False),
                    ('The desire to minimize the number of meetings during development.', False),
                    ('The need to comply with external regulations affecting the organization.', True),
                    ('Switching to a new font in internal documentation.', False),
                ]
            },
            {
                'text': 'Which factor is most likely to be a major driver for initiating system procurement in an organization?',
                'choices': [
                    ('Switching to a new font in internal documentation.', False),
                    ('The desire to minimize the number of meetings during development.', False),
                    ('The need to comply with external regulations affecting the organization.', True),
                    ('Increasing the number of programming languages allowed in the codebase.', False),
                ]
            },
            {
                'text': 'Which option best matches the assurance idea ofexposure limitation and recovery?',
                'choices': [
                    ('Using malware scanners to detect and neutralize attacks before harm occurs.', False),
                    ('Allowing any input format to reduce user friction.', False),
                    ('Disconnecting a system from all networks so external attacks are impossible.', False),
                    ('Maintaining backups and a recovery plan so damaged information can be restored after an incident.', True),
                ]
            },
            {
                'text': 'Which type of system is most likely usable with minimal change and only limited configuration?',
                'choices': [
                    ('An off-the-shelf application that is adopted largely as-is.', True),
                    ('A prototype that exists only as a conceptual design.', False),
                    ('A fully custom system designed and implemented specifically for one organization.', False),
                    ('A configurable ERP that must be adapted by changing business rules and process definitions.', False),
                ]
            },
            {
                'text': 'Which type of system is most likely usable with minimal change and only limited configuration?',
                'choices': [
                    ('A prototype that exists only as a conceptual design.', False),
                    ('A fully custom system designed and implemented specifically for one organization.', False),
                    ('An off-the-shelf application that is adopted largely as-is.', True),
                    ('A configurable ERP that must be adapted by changing business rules and process definitions.', False),
                ]
            },
            {
                'text': 'Which principle best reflects a cost-effective, risk-based approach to security?',
                'choices': [
                    ('Do not spend more on controls than the value of the asset they protect.', True),
                    ('Always implement the strongest possible controls regardless of cost.', False),
                    ('Prioritize aesthetic UI improvements over security controls.', False),
                    ('Remove authentication to reduce development time.', False),
                ]
            },
            {
                'text': 'When a system is built specially by a supplier, why is the requirements specification often considered both a technical and a legal document?',
                'choices': [
                    ('Because legal documents cannot include diagrams or models.', False),
                    ('Because off-the-shelf systems require detailed requirements to be used.', False),
                    ('Because requirements are always written by lawyers and never by engineers.', False),
                    ('Because the specification is part of the development contract, defining what the supplier must deliver and under what terms.', True),
                ]
            },
            {
                'text': 'When a system is built specially by a supplier, why is the requirements specification often considered both a technical and a legal document?',
                'choices': [
                    ('Because off-the-shelf systems require detailed requirements to be used.', False),
                    ('Because the specification is part of the development contract, defining what the supplier must deliver and under what terms.', True),
                    ('Because requirements are always written by lawyers and never by engineers.', False),
                    ('Because legal documents cannot include diagrams or models.', False),
                ]
            },
            {
                'text': 'What is a primary purpose of an organizationalsecurity policy?',
                'choices': [
                    ('To guarantee that no system will ever be attacked.', False),
                    ('To replace all technical design documents with a single long and highly detailed manual.', False),
                    ('To communicate broad security goals and expectations so security decisions are consistent and understandable across the organization.', True),
                    ('To ensure all assets receive the same highest level of protection.', False),
                ]
            },
            {
                'text': 'Large system development efforts often use a plan-driven approach. Which reason best explains this tendency?',
                'choices': [
                    ('Because different parts (hardware, software, communications) are developed in parallel and hardware changes are expensive, limiting iteration between phases.', True),
                    ('Because agile methods cannot be used for any software project.', False),
                    ('Because testing is unnecessary when a plan exists.', False),
                    ('Because plan-driven approaches require no stakeholder input.', False),
                ]
            },
            {
                'text': "Which sequence best matches common stages of security risk assessment across a system's life?",
                'choices': [
                    ('Penetration testing → user training → hardware replacement.', False),
                    ('Preliminary risk assessment → life cycle/design risk assessment → operational risk assessment.', True),
                    ('Operational risk assessment → preliminary risk assessment → life cycle/design risk assessment.', False),
                    ('Code compilation → UI testing → performance benchmarking.', False),
                ]
            },
            {
                'text': 'In a system development process, what doesrequirements partitioningprimarily involve?',
                'choices': [
                    ('Deciding which subsystems are responsible for implementing specific system requirements.', True),
                    ('Writing end-user training materials for operators.', False),
                    ('Selecting a supplier shortlist during procurement.', False),
                    ('ComputingP(fail)=1−Rfor each hardware component.', False),
                ]
            },
            {
                'text': 'In a system development process, what doesrequirements partitioningprimarily involve?',
                'choices': [
                    ('ComputingP(fail)=1−Rfor each hardware component.', False),
                    ('Writing end-user training materials for operators.', False),
                    ('Deciding which subsystems are responsible for implementing specific system requirements.', True),
                    ('Selecting a supplier shortlist during procurement.', False),
                ]
            },
            {
                'text': "A requirement states: 'The system shall detect abnormal login behavior and block the session before any data is accessed.' How is this best classified?",
                'choices': [
                    ('Non-functional performance requirement.', False),
                    ('Risk avoidance requirement.', False),
                    ('Risk mitigation requirement.', False),
                    ('Risk detection requirement.', True),
                ]
            },
            {
                'text': 'Why can increased automation in system operation sometimes raise cost and reduce flexibility?',
                'choices': [
                    ('Because automation eliminates the need for requirements engineering.', False),
                    ('Because automated systems always improve usability and never introduce complexity.', False),
                    ('Because humans cannot be trained to operate systems.', False),
                    ('Because automation requires designing for many anticipated failure modes and automated behavior is less adaptable than humans in unexpected situations.', True),
                ]
            },
            {
                'text': 'Why can increased automation in system operation sometimes raise cost and reduce flexibility?',
                'choices': [
                    ('Because humans cannot be trained to operate systems.', False),
                    ('Because automated systems always improve usability and never introduce complexity.', False),
                    ('Because automation eliminates the need for requirements engineering.', False),
                    ('Because automation requires designing for many anticipated failure modes and automated behavior is less adaptable than humans in unexpected situations.', True),
                ]
            },
            {
                'text': 'What is the primary goal ofpenetration testingin security validation?',
                'choices': [
                    ('To attempt to breach system security by simulating realistic attacks and finding exploitable weaknesses.', True),
                    ('To increase system throughput by removing security checks.', False),
                    ('To replace the need for secure design by adding more servers.', False),
                    ('To prove mathematically that all security requirements are satisfied.', False),
                ]
            },
            {
                'text': 'Which statement best describes asoftware product line?',
                'choices': [
                    ('A set of related applications sharing a common architecture and components, specialized for different requirements.', True),
                    ('A random collection of unrelated apps in an app store.', False),
                    ('A single application that cannot be modified to avoid version fragmentation.', False),
                    ('A system that only reuses design patterns and no actual components.', False),
                ]
            },
            {
                'text': 'Which option best describessystem reusein software engineering?',
                'choices': [
                    ('Reusing only small utility functions such as string helpers.', False),
                    ('Reusing a design idea without any actual software artifacts.', False),
                    ('Reusing complete systems that may include several application programs.', True),
                    ('Reusing a single class by copying its source code into a new project.', False),
                ]
            },
            {
                'text': 'Which statement best captures the essence of a software service in service-based systems?',
                'choices': [
                    ('It always results in transferring ownership of underlying resources to the user.', False),
                    ('It must always be deployed together with its client application.', False),
                    ('It requires all consumers to use the same programming language and platform.', False),
                    ('It delivers functionality that is independent of the application using it.', True),
                ]
            },
            {
                'text': 'Compared with traditional software components, which feature is most characteristic of services in service-based systems?',
                'choices': [
                    ('They must be linked at compile time into a single executable.', False),
                    ('They require a graphical user interface for every operation.', False),
                    ('They can only be accessed through shared-memory method calls.', False),
                    ("They are independent and do not rely on a 'requires' interface.", True),
                ]
            },
            {
                'text': "In a service-oriented approach, what does 'loosely coupled' most directly imply?",
                'choices': [
                    ('Consumers interact through standardized messages rather than internal implementation details.', True),
                    ('Services must run on the same machine as the client.', False),
                    ('All services must share one database schema.', False),
                    ('Interfaces are unnecessary because services are self-describing at runtime in all cases.', False),
                ]
            },
            {
                'text': 'What is a key benefit of delaying the binding of services until deployment or execution?',
                'choices': [
                    ('It eliminates the need for interface documentation.', False),
                    ('It guarantees that no network failures can occur.', False),
                    ('It forces all service providers to use the same internal design.', False),
                    ('Applications can adapt to changes by selecting more appropriate services at runtime.', True),
                ]
            },
            {
                'text': 'In a typical service-oriented architecture, which set of roles is fundamental to how services are published and used?',
                'choices': [
                    ('Browser, DNS server, and certificate authority.', False),
                    ('Database administrator, system operator, and end user.', False),
                    ('Service provider, service requester, and a service registry.', True),
                    ('Compiler, linker, and loader.', False),
                ]
            },
            {
                'text': 'Which pairing correctly matches a common web-service standard to its primary purpose?',
                'choices': [
                    ('WSDL: defining operations, message formats, bindings, and endpoints.', True),
                    ('WS-BPEL: encrypting transport connections using TLS.', False),
                    ('SOAP: specifying business workflows as executable process models.', False),
                    ('UDDI: executing service code in a virtual machine.', False),
                ]
            },
            {
                'text': "In a service description language such as WSDL, which part most directly answers 'where is the service located'?",
                'choices': [
                    ('The abstract interface listing operation names only.', False),
                    ('The message schema types section only.', False),
                    ('The client-side stub code generated by a tool.', False),
                    ('The endpoint information (location of a specific implementation).', True),
                ]
            },
            {
                'text': 'REST (Representational State Transfer) is best described as:',
                'choices': [
                    ('A binary RPC protocol that requires a fixed interface description standard.', False),
                    ('A programming language used only for building web pages.', False),
                    ('A database indexing technique for fast queries.', False),
                    ('An architectural style based on transferring representations of resources from server to client.', True),
                ]
            },
            {
                'text': "In a RESTful architecture, what is a 'resource'?",
                'choices': [
                    ('Only a physical device connected to the network.', False),
                    ('A single immutable file format that cannot change representation.', False),
                    ('A data element identified by a URL and representable in multiple formats (e.g., PDF, HTML).', True),
                    ('Only a server-side thread that handles a request.', False),
                ]
            },
            {
                'text': 'Which mapping between CRUD-style operations and HTTP verbs is most commonly associated with RESTful services?',
                'choices': [
                    ('Create→PUT, Read→DELETE, Update→GET, Delete→POST.', False),
                    ('CRUD does not map to HTTP verbs in RESTful designs.', False),
                    ('Create→POST, Read→GET, Update→PUT, Delete→DELETE.', True),
                    ('Create→GET, Read→POST, Update→DELETE, Delete→PUT.', False),
                ]
            },
            {
                'text': "A RESTful service exposes a collection of resources at a base URL. Which approach is most appropriate for requesting a specific date's data without changing the resource identity?",
                'choices': [
                    ('Use a URL query parameter such as...?date=20250115with GET.', True),
                    ('Use DELETE to indicate the date to retrieve.', False),
                    ('Encode the date in a client-side file name and upload it.', False),
                    ('Send the date only by emailing the service provider.', False),
                ]
            },
            {
                'text': "Which is a commonly cited disadvantage of using RESTful services compared with more formalized 'big web service' stacks?",
                'choices': [
                    ('REST cannot use HTTP or HTTPS as transport protocols.', False),
                    ('REST forces all services to be stateful and session-based.', False),
                    ('REST cannot represent documents or records as resources.', False),
                    ('There is no single standardized way to describe RESTful interfaces, so users may rely on informal documentation.', True),
                ]
            },
            {
                'text': 'Service engineering is primarily concerned with:',
                'choices': [
                    ('Developing dependable, reusable services intended for use across different systems.', True),
                    ('Replacing all network protocols with proprietary ones to reduce interoperability.', False),
                    ('Eliminating the need for testing by using only third-party services.', False),
                    ("Optimizing a single application's user interface for one device type.", False),
                ]
            },
            {
                'text': 'Which sequence best matches typical stages in a service engineering process?',
                'choices': [
                    ('Code obfuscation → UI prototyping → branding review.', False),
                    ('Testing only → deployment only → documentation only.', False),
                    ('Database migration → hardware procurement → office rollout.', False),
                    ('Service candidate identification → service design → service implementation and deployment.', True),
                ]
            },
            {
                'text': 'Which classification correctly distinguishes three fundamental types of services used in service-based systems?',
                'choices': [
                    ('Compile-time services, link-time services, and run-time services.', False),
                    ('Monolithic services, spaghetti services, and untyped services.', False),
                    ('Kernel services, driver services, and firmware services.', False),
                    ('Utility services, business services, and coordination services.', True),
                ]
            },
            {
                'text': 'Which statement best describes task-oriented vs entity-oriented services?',
                'choices': [
                    ('Task-oriented services must always be implemented with SOAP, not REST.', False),
                    ('Task-oriented services store only images, while entity-oriented services store only numbers.', False),
                    ('Entity-oriented services cannot be reused across business processes.', False),
                    ('Task-oriented services focus on activities, while entity-oriented services focus on business entities such as forms or records.', True),
                ]
            },
            {
                'text': 'Which statement is most accurate about coordination services in service-based systems?',
                'choices': [
                    ('They only provide general-purpose utilities such as currency conversion.', False),
                    ('They support composite business processes and are always task-oriented.', True),
                    ('They cannot be implemented using workflows.', False),
                    ('They are always entity-oriented and never include control flow.', False),
                ]
            },
            {
                'text': 'When identifying potential services, which question is most directly about service independence and external reuse?',
                'choices': [
                    ('Does the service require a specific brand of keyboard?', False),
                    ('Could the service be used by clients outside the organisation?', True),
                    ('Should the logo be redesigned before deployment?', False),
                    ('Will all users always have identical non-functional requirements?', False),
                ]
            },
            {
                'text': 'Which design principle best aligns with efficient service interface design?',
                'choices': [
                    ('Maximize the number of round trips so that each field is confirmed separately.', False),
                    ('Hide all errors by returning success for every request.', False),
                    ('Use different message formats for every consumer to avoid standardization.', False),
                    ('Minimize the number of messages needed to complete a service request.', True),
                ]
            },
            {
                'text': 'A service must handle up torrequests per second. If each request triggerskinternal operations, what is the required internal operation rate (operations/second)?',
                'choices': [
                    ('λ=r−k', False),
                    ('λ=r+k', False),
                    ('λ=rk', False),
                    ('λ=r×k', True),
                ]
            },
            {
                'text': "Why do many organizations choose RESTful services over more 'heavyweight' web-service stacks in some cases?",
                'choices': [
                    ('They require no URLs because resources are addressed by memory pointer.', False),
                    ('They completely eliminate the need for any transport protocol.', False),
                    ('They guarantee perfect reliability without monitoring or management.', False),
                    ('They tend to be simpler and impose lower overhead for many web-based scenarios.', True),
                ]
            },
            {
                'text': 'How can service-based systems help preserve investment in existing (legacy) systems?',
                'choices': [
                    ('By preventing any external applications from accessing legacy functions.', False),
                    ('By deleting legacy systems and rewriting everything from scratch.', False),
                    ('By forcing legacy code to be converted into a mobile app UI.', False),
                    ('By implementing service interfaces that provide access to legacy functionality.', True),
                ]
            },
            {
                'text': 'Which item is most important to include in a public service description to help potential users decide whether to trust and adopt the service?',
                'choices': [
                    ('The personal social media preferences of each developer.', False),
                    ('An instruction to ignore updates and never change the interface.', False),
                    ('A requirement that all users must reveal their passwords to support staff.', False),
                    ('Provider information and contact details, alongside clear usage documentation.', True),
                ]
            },
            {
                'text': 'In service composition, what is most commonly used as the basis for coordinating multiple services into a coherent business process?',
                'choices': [
                    ('A single monolithic function that merges all service code into one file.', False),
                    ('A manual checklist executed only by end users without automation.', False),
                    ('A requirement that all services share the same database transaction.', False),
                    ('A workflow describing the logical sequence of activities and service interactions.', True),
                ]
            },
            {
                'text': 'Which statement best reflects the relationship between WS-BPEL and graphical workflow notations such as BPMN?',
                'choices': [
                    ('WS-BPEL specifications can be lengthy, so graphical notations like BPMN are used for readability and may be compiled into WS-BPEL.', True),
                    ('Graphical workflow models cannot be used with RESTful services.', False),
                    ('WS-BPEL is used only for encrypting SOAP messages.', False),
                    ('BPMN is a network transport protocol that replaces HTTP.', False),
                ]
            },
            {
                'text': 'Which sequence best represents a typical high-level process for constructing a composite service by composition?',
                'choices': [
                    ('Formulate outline workflow → discover services → select services → refine workflow → create executable workflow/program → test.', True),
                    ('Select services → delete registry → disable monitoring → deploy.', False),
                    ('Write WSDL → always use SOAP → never refine workflow → stop.', False),
                    ('Buy hardware → rename variables → skip testing → publish marketing page.', False),
                ]
            },
            {
                'text': 'Why is testing a composed application that uses external services often more difficult than testing an in-house component library?',
                'choices': [
                    ('Because external services always provide full source code for white-box testing.', False),
                    ('Because dynamic binding guarantees the same service instance is always used in every test.', False),
                    ("External services are 'black-boxes', may change, and their non-functional behavior can vary with load.", True),
                    ('Because service testing is free of charge in all pay-per-use models.', False),
                ]
            },
            {
                'text': 'Which feature is commonly provided by modern web application frameworks to support interactive pages?',
                'choices': [
                    ('Mandatory use of assembly language for page templates.', False),
                    ('Eliminating the need for authentication and access control.', False),
                    ('AJAX support that enables more interactive web pages.', True),
                    ('Replacing databases with plain text files in all deployments.', False),
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
                self.stdout.write(f'  Added question {idx}: {q_data["text"][:50]}...')
            else:
                self.stdout.write(f'  Question {idx} already exists: {q_data["text"][:50]}...')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(questions_data)} questions. '
                f'{added_count} new questions added, {len(questions_data) - added_count} already existed.'
            )
        )
