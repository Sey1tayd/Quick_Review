from django.core.management.base import BaseCommand
from quiz.models import Course, Session, Question, Choice
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Adds questions for COMP 3226 - XR Technologies: Metaverse, AR and VR'

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            slug='comp3226',
            defaults={
                'title': 'COMP 3226 - XR Technologies',
                'description': 'Metaverse, AR and VR'
            }
        )
        self.stdout.write(f'Course: {course.title}')

        sessions_data = [
            {
                'title': 'Introduction to XR Technologies',
                'questions': [
                    {
                        'text': 'What does the "X" in XR stands for?',
                        'choices': [
                            ('x-treme', False),
                            ('x-ray', False),
                            ('extended(as a variable for any reality)', True),
                            ('x-large', False),
                        ]
                    },
                    {
                        'text': 'How does XR impact the classroom?',
                        'choices': [
                            ('Lessons in VR improve memory and student engagement.', True),
                            ('Reading books is better for long term learning.', False),
                            ('Simple slides are more effective than 3D tools.', False),
                            ('Digital files are hard for students to manage.', False),
                        ]
                    },
                    {
                        'text': 'Which mode offers total isolation?',
                        'choices': [
                            ('Fully digital world', True),
                            ('Real space', False),
                            ('Video frames', False),
                            ('Static view', False),
                        ]
                    },
                    {
                        'text': 'How does MR handle objects?',
                        'choices': [
                            ('Simple data', False),
                            ('Successful interaction', True),
                            ('Visual only', False),
                            ('Low speed', False),
                        ]
                    },
                    {
                        'text': 'What defines Telepresence for teams?',
                        'choices': [
                            ('Social apps for sending quick messages.', False),
                            ('Video calls on a standard laptop screen.', False),
                            ('Phone chats using mobile data signals.', False),
                            ('Meeting in VR to feel like being together.', True),
                        ]
                    },
                    {
                        'text': 'What does PPD measure?',
                        'choices': [
                            ('Assessment of clarity', True),
                            ('Image speed', False),
                            ('Power data', False),
                            ('Price point', False),
                        ]
                    },
                    {
                        'text': 'A narrow FOV feels like?',
                        'choices': [
                            ('Fast motion', False),
                            ('Clear view', False),
                            ('Wide angle', False),
                            ('Tunnel-like vision', True),
                        ]
                    },
                    {
                        'text': 'Why is latency a problem for users?',
                        'choices': [
                            ('Motion blur happens only in dark rooms.', False),
                            ('High price makes the hardware hard to buy.', False),
                            ('Dizziness occurs when the visual lag is high.', True),
                            ('Visual data is too bright for the human eye.', False),
                        ]
                    },
                    {
                        'text': 'Why use XR in surgery?',
                        'choices': [
                            ('Video study', False),
                            ('Error-free practice', True),
                            ('Simple tools', False),
                            ('High risk', False),
                        ]
                    },
                    {
                        'text': 'What is the role of a Digital Twin?',
                        'choices': [
                            ('Accurate models that predict system failures.', True),
                            ('Basic copies for simple marketing plans.', False),
                            ('Virtual images used for social media posts.', False),
                            ('Manual data entry for factory workers.', False),
                        ]
                    },
                    {
                        'text': 'Why use Unity or Unreal?',
                        'choices': [
                            ('Basic app', False),
                            ('Simple web', False),
                            ('Common 3D tools', True),
                            ('Code only', False),
                        ]
                    },
                    {
                        'text': 'How to make lighter XR headsets?',
                        'choices': [
                            ('Using heavy metal to protect the glass.', False),
                            ('Building larger batteries into the frames.', False),
                            ('Fast cables connected to a desktop PC.', False),
                            ('Offloading data to Cloud servers via 5G.', True),
                        ]
                    },
                    {
                        'text': 'Apple Vision Pro belongs to?',
                        'choices': [
                            ('Basic lenses', False),
                            ('Appearing as hybrid', True),
                            ('Simple tool', False),
                            ('Retro gear', False),
                        ]
                    },
                    {
                        'text': 'What is the Reality-Virtuality Continuum?',
                        'choices': [
                            ('All reality stages from physical to virtual.', True),
                            ('Digital speed of the modern internet.', False),
                            ('Mixed history of computer hardware.', False),
                            ('Future costs of global tech products.', False),
                        ]
                    },
                    {
                        'text': 'What does AR do on a phone?',
                        'choices': [
                            ('Mobile gaming', False),
                            ('Virtual world', False),
                            ('Static image', False),
                            ('Adding digital items', True),
                        ]
                    },
                    {
                        'text': "What is AI's job in spatial mapping?",
                        'choices': [
                            ('Tracking people in a very bright environment.', False),
                            ('Reading text from a static digital screen.', False),
                            ('Mapping rooms to place objects accurately.', True),
                            ('Photo storage for the internal memory.', False),
                        ]
                    },
                    {
                        'text': 'What is the market forecast for 2030?',
                        'choices': [
                            ('Market sales will drop to zero very fast.', False),
                            ('Billion dollar growth in the global sector.', True),
                            ('Small niche for specialized gamers only.', False),
                            ('Local trade will stop due to low interest.', False),
                        ]
                    },
                    {
                        'text': 'What is a top privacy risk in XR?',
                        'choices': [
                            ('Accessing biometric data like eye movements.', True),
                            ('Private photos being shared on social media.', False),
                            ('Security signals blocking the wi-fi speed.', False),
                            ('Digital colors causing eye strain over time.', False),
                        ]
                    },
                    {
                        'text': 'What is the core idea of XR?',
                        'choices': [
                            ('Mixed tech', False),
                            ('Simple data', False),
                            ('All-encompassing reality', True),
                            ('Extra vision', False),
                        ]
                    },
                    {
                        'text': 'How does Spatial Audio help immersion?',
                        'choices': [
                            ('Music volume staying at a very high level.', False),
                            ('Digital signals sent in mono sound mode.', False),
                            ('Loud sounds used to scare the virtual user.', False),
                            ('Addressing sound sources in 3d locations.', True),
                        ]
                    },
                    {
                        'text': 'What does "6DoF" (Six Degrees of Freedom) mean in XR systems?',
                        'choices': [
                            ('Six different screen colors', False),
                            ('Movement in three axes + rotation in three axes', True),
                            ('Six users connected', False),
                            ('Six different sensors only', False),
                        ]
                    },
                    {
                        'text': 'Which factor most directly improves visual smoothness in VR experiences?',
                        'choices': [
                            ('Higher frame rate (FPS)', True),
                            ('Larger file size', False),
                            ('More storage space', False),
                            ('Louder audio', False),
                        ]
                    },
                    {
                        'text': 'Which field benefits from XR by allowing safe simulation of risky scenarios?',
                        'choices': [
                            ('Healthcare', False),
                            ('Aviation training', False),
                            ('Military training', False),
                            ('All of the above', True),
                        ]
                    },
                    {
                        'text': 'Which sensor type helps XR devices understand depth and 3D space?',
                        'choices': [
                            ('Temperature sensor', False),
                            ('Speaker', False),
                            ('Depth sensor', True),
                            ('Battery indicator', False),
                        ]
                    },
                    {
                        'text': 'Which of the following is an example of a VR application?',
                        'choices': [
                            ('Pokemon Go', False),
                            ('Half-Life: Alyx', True),
                            ('Google Maps Street View', False),
                            ('PDF Reader', False),
                        ]
                    },
                    {
                        'text': 'Which component is primarily responsible for detecting head movement in VR headsets?',
                        'choices': [
                            ('IMU (Inertial Measurement Unit)', True),
                            ('Printer driver', False),
                            ('USB cable', False),
                            ('Microphone', False),
                        ]
                    },
                    {
                        'text': 'Why are SLAM (Simultaneous Localization and Mapping) algorithms used in XR technologies?',
                        'choices': [
                            ('To compress files', False),
                            ('To reduce graphic quality', False),
                            ("To determine the device's position and map the environment simultaneously", True),
                            ('To increase internet speed', False),
                        ]
                    },
                    {
                        'text': 'A hologram interacts with a real table and hand movements. Which technology is this?',
                        'choices': [
                            ('VR', False),
                            ('AR', False),
                            ('360° Video', False),
                            ('MR', True),
                        ]
                    },
                    {
                        'text': 'If a headset completely blocks the real world, which technology is it?',
                        'choices': [
                            ('AR', False),
                            ('VR', True),
                            ('MR', False),
                            ('XR', False),
                        ]
                    },
                    {
                        'text': 'Which of the following factors most significantly increases the level of "immersion" in XR technologies?',
                        'choices': [
                            ('Real-time motion (tracking)', True),
                            ('High-resolution display', False),
                            ('Large file size', False),
                            ('High internet data quota', False),
                        ]
                    },
                    {
                        'text': 'If the image lags when a user turns their head in an XR system, what does this indicate?',
                        'choices': [
                            ('Low resolution', False),
                            ('Low storage capacity', False),
                            ('Excess GPU power', False),
                            ('High latency (delay)', True),
                        ]
                    },
                    {
                        'text': 'Which sector is expected to experience the greatest transformation in the future due to XR technologies?',
                        'choices': [
                            ('Healthcare', False),
                            ('Defense', False),
                            ('All of the above', True),
                            ('Education', False),
                        ]
                    },
                    {
                        'text': 'Why is Microsoft HoloLens different from traditional VR headsets?',
                        'choices': [
                            ('It is only used for gaming', False),
                            ('It produces holograms that interact with the physical environment', True),
                            ('It completely blocks the real world', False),
                            ('It cannot connect to the internet', False),
                        ]
                    },
                    {
                        'text': 'What is the purpose of hand tracking in XR?',
                        'choices': [
                            ('To allow interaction without physical controllers', True),
                            ('To monitor internet usage', False),
                            ('To increase storage', False),
                            ('To improve battery charging', False),
                        ]
                    },
                    {
                        'text': 'Which hardware component is responsible for rendering graphics in XR systems?',
                        'choices': [
                            ('CPU', False),
                            ('Microphone', False),
                            ('GPU', True),
                            ('Router', False),
                        ]
                    },
                    {
                        'text': 'Which software is commonly used to develop VR applications?',
                        'choices': [
                            ('Word', False),
                            ('Excel', False),
                            ('Photoshop', False),
                            ('Unity', True),
                        ]
                    },
                    {
                        'text': 'Which of the following institutions supports XR and simulation research projects in Turkey?',
                        'choices': [
                            ('Turkish Airlines', True),
                            ('TÜBİTAK', False),
                            ('ASELSAN', False),
                            ('Ministry of Culture and Tourism', False),
                        ]
                    },
                    {
                        'text': 'What does VR stand for?',
                        'choices': [
                            ('Virtual Reality', True),
                            ('Visual Response', False),
                            ('Virtual Router', False),
                            ('Video Recording', False),
                        ]
                    },
                    {
                        'text': 'What is the main difference between AR and VR?',
                        'choices': [
                            ('AR blocks the real world', False),
                            ('VR adds digital objects to the real world', False),
                            ('AR overlays digital content onto the real world', True),
                            ('VR uses smartphones only', False),
                        ]
                    },
                    {
                        'text': 'In VR, to reduce motion sickness during quick movements, which is most important?',
                        'choices': [
                            ('Low frame rate + high latency', False),
                            ('High resolution + high latency', False),
                            ('Low resolution + low refresh rate', False),
                            ('High frame rate + low latency', True),
                        ]
                    },
                ]
            },
            {
                'title': 'Exploring the Metaverse Concept',
                'questions': [
                    {
                        'text': 'Who popularized the term "metaverse" in the 1992 science fiction novel Snow Crash?',
                        'choices': [
                            ('Neal Stephenson', True),
                            ('Morton Heilig', False),
                            ('Ivan Sutherland', False),
                            ('Neal Armstrong', False),
                        ]
                    },
                    {
                        'text': 'Which 1956 invention introduced multisensory immersive experiences, including sight, sound, touch, and smell?',
                        'choices': [
                            ('Sword of Damocles', False),
                            ('Sensorama', True),
                            ('Oculus Rift', False),
                            ('Second Life', False),
                        ]
                    },
                    {
                        'text': "What is the name of Ivan Sutherland's 1968 head-mounted display featuring motion tracking?",
                        'choices': [
                            ('Active Worlds', False),
                            ('Sensorama', False),
                            ('Sword of Damocles', True),
                            ('Quest 3', False),
                        ]
                    },
                    {
                        'text': 'According to the slides, what is the definition of a "Collective Virtual Space"?',
                        'choices': [
                            ('A persistent, shared digital universe merging physical and virtual realities', True),
                            ('A single-player offline game environment', False),
                            ('A social media platform for sharing photos only', False),
                            ('A physical office space with high-speed internet', False),
                        ]
                    },
                    {
                        'text': 'Which term describes the umbrella encompassing VR, AR, and MR technologies?',
                        'choices': [
                            ('Artificial Intelligence (AI)', False),
                            ('Extended Reality (XR)', True),
                            ('Blockchain Infrastructure', False),
                            ('Digital Ecosystems', False),
                        ]
                    },
                    {
                        'text': 'Which technology enables NFTs for verifiable asset ownership and cryptocurrency for virtual economies?',
                        'choices': [
                            ('5G Networks', False),
                            ('Cloud Computing', False),
                            ('Blockchain', True),
                            ('Haptic Feedback', False),
                        ]
                    },
                    {
                        'text': 'In the technical architecture, which layer includes game engines like Unity and Unreal Engine 5?',
                        'choices': [
                            ('Layer 1: Hardware Layer', False),
                            ('Layer 4: Protocol Layer', False),
                            ('Layer 2: Network Layer', False),
                            ('Layer 3: Engine Layer', True),
                        ]
                    },
                    {
                        'text': 'What is the projected global metaverse market value by 2030?',
                        'choices': [
                            ('$150 Billion', False),
                            ('$800 Billion', True),
                            ('$500 Billion', False),
                            ('$1 Trillion', False),
                        ]
                    },
                    {
                        'text': 'Major technology firms have already committed over how much to metaverse R&D?',
                        'choices': [
                            ('$10 Billion', False),
                            ('$150 Billion', True),
                            ('$100 Billion', False),
                            ('$50 Billion', False),
                        ]
                    },
                    {
                        'text': 'In manufacturing, what are real-time mirrored simulations of production systems called?',
                        'choices': [
                            ('Virtual Prototyping', False),
                            ('Smart Contracts', False),
                            ('Digital Twins', True),
                            ('Holograms', False),
                        ]
                    },
                    {
                        'text': 'Which sector uses "Therapeutic VR" to treat phobias, PTSD, and chronic pain?',
                        'choices': [
                            ('Healthcare', True),
                            ('Architecture', False),
                            ('Education', False),
                            ('Retail', False),
                        ]
                    },
                    {
                        'text': 'Which challenge involves extensive biometric and behavioral data collection risks?',
                        'choices': [
                            ('Technical Limitations', False),
                            ('Regulatory Gaps', False),
                            ('Privacy Concerns', True),
                            ('Addiction Risks', False),
                        ]
                    },
                    {
                        'text': 'What causes "Cybersickness" in XR environments?',
                        'choices': [
                            ('High frame rates', False),
                            ('Visual-vestibular mismatch', True),
                            ('Low battery life', False),
                            ('Fast internet connection', False),
                        ]
                    },
                    {
                        'text': 'To prevent discomfort and maintain presence, motion-to-photon latency must remain below:',
                        'choices': [
                            ('100ms', False),
                            ('20ms', True),
                            ('5ms', False),
                            ('50ms', False),
                        ]
                    },
                    {
                        'text': 'What is the typical Field of View (FOV) for current XR devices compared to human peripheral vision?',
                        'choices': [
                            ('45-60° vs. ~100°', False),
                            ('10-20° vs. ~50°', False),
                            ('90-120° vs. ~200°', True),
                            ('180-200° vs. ~360°', False),
                        ]
                    },
                    {
                        'text': 'What does "Platform Interoperability" refer to in future projections?',
                        'choices': [
                            ('Seamless user mobility across metaverse platforms through open standards', True),
                            ('Users staying on only one platform forever', False),
                            ('Increasing hardware costs for new users', False),
                            ('Limiting user access to corporate entities', False),
                        ]
                    },
                    {
                        'text': 'Predictive maintenance using digital twins can reduce unplanned downtime by how much?',
                        'choices': [
                            ('10%', False),
                            ('25%', False),
                            ('50%', True),
                            ('75%', False),
                        ]
                    },
                    {
                        'text': 'Which layer of technical architecture includes 5G/6G networks and edge computing?',
                        'choices': [
                            ('Layer 1: Hardware Layer', False),
                            ('Layer 2: Network & Infrastructure Layer', True),
                            ('Layer 5: Experience Layer', False),
                            ('Layer 3: Engine Layer', False),
                        ]
                    },
                    {
                        'text': 'What is "Mixed Reality" (MR)?',
                        'choices': [
                            ('A social media app for 3D photos', False),
                            ('Digital information overlays on real-world environments', False),
                            ('Fully immersive digital environments blocking external stimuli', False),
                            ('Seamless integration of virtual and real elements enabling interactive holograms', True),
                        ]
                    },
                    {
                        'text': 'Which ethical framework component ensures user control over personal data and transparent practices?',
                        'choices': [
                            ('Inclusivity & Accessibility', False),
                            ('Privacy & Data Ownership', True),
                            ('Psychological Safety', False),
                            ('Engineering Responsibility', False),
                        ]
                    },
                    {
                        'text': 'Which structural feature allows digital assets to be moved freely between different Metaverse platforms?',
                        'choices': [
                            ('Salability', False),
                            ('Persistence', False),
                            ('Interoperability', True),
                            ('Holographic projection', False),
                        ]
                    },
                    {
                        'text': 'What is the most critical value that Web 3.0 technology adds to the Metaverse ecosystem?',
                        'choices': [
                            ('Faster internet connection speeds', False),
                            ('Ownership of digital assets', True),
                            ('Advanced 3D graphics rendering', False),
                            ('Centralized server usage', False),
                        ]
                    },
                    {
                        'text': 'In the context of the Metaverse, what do "Digital Twins" represent?',
                        'choices': [
                            ('Two different characters used by the same person', False),
                            ('Virtual replicas of physical objects or entire cities', True),
                            ('The ability to exist in two different worlds at once', False),
                            ('Avatars controlled by two users simultaneously', False),
                        ]
                    },
                    {
                        'text': 'What are the 4 key points that make the Metaverse different from a simple 3D game?',
                        'choices': [
                            ('Presence, interoperability, persistence, economy', True),
                            ('Speed, graphics, sound, score', False),
                            ('Ads, likes, comments, followers', False),
                            ('Password, email, camera, screen', False),
                        ]
                    },
                    {
                        'text': 'What does "presence" mean in the Metaverse?',
                        'choices': [
                            ('Using only a keyboard', False),
                            ('Having many apps on your phone', False),
                            ('Watching a video in 2D', False),
                            ('Feeling you are inside the virtual world', True),
                        ]
                    },
                    {
                        'text': 'What does "persistence" mean?',
                        'choices': [
                            ('The world is always offline', False),
                            ('The world is only a short video', False),
                            ('The world continues when you log out', True),
                            ('The world has no users', False),
                        ]
                    },
                    {
                        'text': "Which term describes the psychological feeling of actually 'being inside' a virtual world?",
                        'choices': [
                            ('Latency', False),
                            ('Presence', True),
                            ('Haptics', False),
                            ('Bandwidth', False),
                        ]
                    },
                    {
                        'text': 'What do we call a virtual replica of a physical object, factory, or city?',
                        'choices': [
                            ('Digital Twin', True),
                            ('NFT', False),
                            ('Smart Contract', False),
                            ('Game Engine', False),
                        ]
                    },
                    {
                        'text': "What does 'Interoperability' mean in the Metaverse ecosystem?",
                        'choices': [
                            ('Playing games offline', False),
                            ('Wearing VR headsets wirelessly', False),
                            ('Moving digital assets between different worlds', True),
                            ('Buying virtual land with cash', False),
                        ]
                    },
                    {
                        'text': 'Why is an avatar in the metaverse more than a profile picture?',
                        'choices': [
                            ('It is only decorative', False),
                            ('It is required mainly to match users with ads', False),
                            ('It acts like a digital body, carrying identity, expression, and interaction', True),
                            ('It is only needed in games, not in the metaverse', False),
                        ]
                    },
                    {
                        'text': 'What is the best reason people pay for digital fashion/skins in the metaverse?',
                        'choices': [
                            ('Real money cannot be used in the metaverse', False),
                            ('They signal identity, status, and belonging in visible social spaces', True),
                            ('Virtual items are more durable than physical goods', False),
                            ('Governments require people to buy virtual items', False),
                        ]
                    },
                    {
                        'text': 'Which combination most strongly increases social presence in the metaverse?',
                        'choices': [
                            ('Faster internet + cheaper devices', False),
                            ('Higher resolution + brighter colors', False),
                            ('More menus + more settings options', False),
                            ('Spatial audio + distance/direction cues + nonverbal signals', True),
                        ]
                    },
                    {
                        'text': 'What is the primary concern regarding "Biometric Data" in the Metaverse compared to the traditional internet?',
                        'choices': [
                            ('It tracks physical movements, eye tracking, and emotional responses.', True),
                            ('It only tracks your IP address.', False),
                            ('It is only used for avatar skin colors.', False),
                            ('It is impossible to collect in 3D spaces.', False),
                        ]
                    },
                    {
                        'text': 'What does "Decentralized Governance" mean for a Metaverse platform?',
                        'choices': [
                            ('A single company (like Meta) makes all the rules', False),
                            ('The government of a specific country controls the platform', False),
                            ('The users/community vote on the rules and changes of the world', True),
                            ('There are no rules at all in the virtual world', False),
                        ]
                    },
                    {
                        'text': 'According to the "Human-Centric" vision of the Metaverse, what should be the primary goal?',
                        'choices': [
                            ('To maximize corporate profits.', False),
                            ('To replace the physical world entirely.', False),
                            ('To create a place where law does not exist.', False),
                            ('To solve real-world problems and enhance human connection.', True),
                        ]
                    },
                    {
                        'text': 'Which component enables real-time interaction between users through voice, gestures, and movement in the metaverse?',
                        'choices': [
                            ('Static Rendering', False),
                            ('Real-Time Interaction Systems', True),
                            ('Offline Processing', False),
                            ('Data Compression', False),
                        ]
                    },
                    {
                        'text': 'What is the main purpose of haptic feedback in XR environments?',
                        'choices': [
                            ('To improve internet speed', False),
                            ('To simulate touch and physical sensations', True),
                            ('To reduce storage usage', False),
                            ('To display higher resolution images', False),
                        ]
                    },
                    {
                        'text': 'Which concept refers to a self-sustaining virtual economy with buying, selling, and trading?',
                        'choices': [
                            ('Digital Identity', False),
                            ('Virtual Economy', True),
                            ('Cloud Storage', False),
                            ('Network Layer', False),
                        ]
                    },
                    {
                        'text': 'What role do avatars play in social interaction within the metaverse?',
                        'choices': [
                            ('They replace all real-world communication permanently', False),
                            ('They act as visual representations enabling interaction and expression', True),
                            ('They only function as gaming characters with no social role', False),
                            ('They are used only for system testing', False),
                        ]
                    },
                    {
                        'text': 'Which factor is most important for achieving realism in virtual environments?',
                        'choices': [
                            ('Low battery consumption', False),
                            ('High latency', False),
                            ('Accurate physics and rendering', True),
                            ('Limited user interaction', False),
                        ]
                    },
                ]
            },
            {
                'title': 'Technical Foundations of XR: Hardware and Software',
                'questions': [
                    {
                        'text': 'What is XR described as in the presentation?',
                        'choices': [
                            ('The Next Step in Gaming', False),
                            ('The Ultimate Magic Trick', True),
                            ('The Future of the Internet', False),
                            ('A New Type of Screen', False),
                        ]
                    },
                    {
                        'text': 'In Mixed Reality (MR), what makes it different from AR?',
                        'choices': [
                            ('It fully replaces the real world', False),
                            ('It only works outdoors', False),
                            ('Digital and real-world items can interact with each other', True),
                            ('It uses no screens', False),
                        ]
                    },
                    {
                        'text': 'How do VR headsets trick human eyes?',
                        'choices': [
                            ('They use holograms', False),
                            ('They put screens very close to the eyes', True),
                            ('They project images onto walls', False),
                            ('They use special contact lenses', False),
                        ]
                    },
                    {
                        'text': 'What technology do most VR headsets use for their screens?',
                        'choices': [
                            ('Plasma or CRT', False),
                            ('OLED or LCD', True),
                            ('E-Ink or LED', False),
                            ('Laser or Hologram', False),
                        ]
                    },
                    {
                        'text': 'Why do VR headsets show a separate image to each eye?',
                        'choices': [
                            ('To reduce battery usage', False),
                            ('To create fake 3D depth', True),
                            ('To increase brightness', False),
                            ('To reduce eye strain', False),
                        ]
                    },
                    {
                        'text': 'What type of lenses do VR headsets use?',
                        'choices': [
                            ('Concave lenses', False),
                            ('Bifocal lenses', False),
                            ('Fresnel lenses', True),
                            ('Convex lenses', False),
                        ]
                    },
                    {
                        'text': 'What is "Presence" in XR?',
                        'choices': [
                            ('The screen surrounding you completely', False),
                            ('The deep psychological feeling of physically standing in a new place', True),
                            ('The refresh rate of the display', False),
                            ('The number of sensors in the headset', False),
                        ]
                    },
                    {
                        'text': 'What does IMU stand for?',
                        'choices': [
                            ('Integrated Motion Unit', False),
                            ('Internal Mapping Unit', False),
                            ('Inertial Measurement Unit', True),
                            ('Image Management Utility', False),
                        ]
                    },
                    {
                        'text': 'How many times per second do IMU chips sample your movement?',
                        'choices': [
                            ('100 times', False),
                            ('500 times', False),
                            ('1,000 times', True),
                            ('10,000 times', False),
                        ]
                    },
                    {
                        'text': 'What does 3DoF only track?',
                        'choices': [
                            ('Physical movement (walking)', False),
                            ('Eye movement', False),
                            ('Rotation only', True),
                            ('Hand gestures', False),
                        ]
                    },
                    {
                        'text': 'What physical movements does 6DoF add beyond rotation?',
                        'choices': [
                            ('Eye blinking and breathing', False),
                            ('Surge, strafe, and elevation', True),
                            ('Pitch, yaw, and roll', False),
                            ('Swimming and jumping', False),
                        ]
                    },
                    {
                        'text': 'What is Inside-Out Tracking also called?',
                        'choices': [
                            ('GPS Mapping', False),
                            ('SLAM', True),
                            ('IMU Scan', False),
                            ('6DoF Vision', False),
                        ]
                    },
                    {
                        'text': 'What is XR described as — pre-recorded video or something else?',
                        'choices': [
                            ('A pre-recorded video loop', False),
                            ('A live mathematical simulation', True),
                            ('A 360-degree photograph', False),
                            ('An AI-generated film', False),
                        ]
                    },
                    {
                        'text': 'Which two game engines dominate the XR industry?',
                        'choices': [
                            ('Godot and CryEngine', False),
                            ('Source and Frostbite', False),
                            ('Unity and Unreal', True),
                            ('Roblox and GameMaker', False),
                        ]
                    },
                    {
                        'text': 'What programming language does Unity use?',
                        'choices': [
                            ('Python', False),
                            ('Java', False),
                            ('C#', True),
                            ('C++', False),
                        ]
                    },
                    {
                        'text': 'What is the maximum allowed latency for VR before cybersickness occurs?',
                        'choices': [
                            ('7 milliseconds', False),
                            ('20 milliseconds', True),
                            ('50 milliseconds', False),
                            ('100 milliseconds', False),
                        ]
                    },
                    {
                        'text': 'What is "Asynchronous Timewarp"?',
                        'choices': [
                            ('A new type of VR headset', False),
                            ('A trick that bends the last frame to match your new head position', True),
                            ('A sensor that measures latency', False),
                            ('A game engine plugin', False),
                        ]
                    },
                    {
                        'text': 'What do tiny motors (actuators) do in haptic controllers?',
                        'choices': [
                            ('Generate heat to simulate warmth', False),
                            ('Create physical vibrations and forces to simulate touch', True),
                            ('Track hand position with cameras', False),
                            ('Charge the headset wirelessly', False),
                        ]
                    },
                    {
                        'text': 'What does "Spatial Computing" mean according to the presentation?',
                        'choices': [
                            ('Computing done in outer space', False),
                            ('Digitizing daily activities and placing them in the room with you', True),
                            ('Using a computer to map underground spaces', False),
                            ('A new type of cloud computing', False),
                        ]
                    },
                    {
                        'text': 'What pixel density are future Retina-Resolution Displays reaching?',
                        'choices': [
                            ('5,000 pixels per inch', False),
                            ('10,000 pixels per inch', False),
                            ('25,000 pixels per inch', True),
                            ('100,000 pixels per inch', False),
                        ]
                    },
                    {
                        'text': 'What does the term XR (Extended Reality) include?',
                        'choices': [
                            ('Only Virtual Reality', False),
                            ('Virtual Reality and Augmented Reality', False),
                            ('Virtual Reality, Augmented Reality, and Mixed Reality', True),
                            ('Only Mixed Reality', False),
                        ]
                    },
                    {
                        'text': 'What is the main difference between AR and MR?',
                        'choices': [
                            ('AR creates a fully virtual environment', False),
                            ('MR understands the physical environment and anchors digital objects to it', True),
                            ('AR only works with headsets', False),
                            ('MR does not use sensors', False),
                        ]
                    },
                    {
                        'text': 'What is the primary purpose of foveated rendering?',
                        'choices': [
                            ('To increase latency', False),
                            ('To expand the field of view', False),
                            ('To improve performance by rendering the gaze area in high resolution', True),
                            ('To replace the GPU', False),
                        ]
                    },
                    {
                        'text': 'What is the function of a SoC (System on Chip) in XR devices?',
                        'choices': [
                            ('It only processes audio', False),
                            ('It provides internet connectivity', False),
                            ('It integrates CPU, GPU, and other components into a single chip', True),
                            ('It replaces motion tracking systems', False),
                        ]
                    },
                    {
                        'text': 'Which of the following is an XR interaction device?',
                        'choices': [
                            ('Cloud server', False),
                            ('Motion controller', True),
                            ('Rendering engine', False),
                            ('SLAM algorithm', False),
                        ]
                    },
                    {
                        'text': 'Which two main components of Virtual Reality systems are focused on in the presentation?',
                        'choices': [
                            ('GPU and Cloud Rendering', False),
                            ('Head-Mounted Displays and Sensors & Tracking Systems', True),
                            ('Motion Controllers and Haptic Gloves', False),
                            ('Edge Computing and Networking', False),
                        ]
                    },
                    {
                        'text': 'What is the main function of a Head-Mounted Display (HMD) in Virtual Reality?',
                        'choices': [
                            ('To connect VR systems to the internet', False),
                            ('To store virtual environments', False),
                            ('To show VR and track head movement', True),
                            ('To control motion controllers', False),
                        ]
                    },
                    {
                        'text': 'Why is VR useful for medical students?',
                        'choices': [
                            ('It replaces real hospitals', False),
                            ('It reduces the need for doctors', False),
                            ('It allows safe practice of surgical procedures', True),
                            ('It automatically performs surgeries', False),
                        ]
                    },
                    {
                        'text': 'What is the main advantage of VR flight simulators for pilots?',
                        'choices': [
                            ('They eliminate the need for real flights', False),
                            ('They reduce the cost of airplanes', False),
                            ('They automatically control the aircraft', False),
                            ('They allow pilots to train in realistic flight conditions', True),
                        ]
                    },
                    {
                        'text': 'What is a key advantage of inside-out tracking in VR systems?',
                        'choices': [
                            ('It requires many external sensors', False),
                            ('It only works in large spaces', False),
                            ('It uses cameras on the headset and needs no external sensors', True),
                            ('It only tracks hand movements', False),
                        ]
                    },
                    {
                        'text': 'What is the main purpose of OpenXR?',
                        'choices': [
                            ('To create exclusive APIs for each XR device', False),
                            ('To act as a universal, royalty-free API for XR devices', True),
                            ('To replace Meta hardware entirely', False),
                            ('To make VR hardware obsolete', False),
                        ]
                    },
                    {
                        'text': 'Which statement about OpenXR adoption is correct?',
                        'choices': [
                            ('Only supports Valve and HTC devices', False),
                            ('Requires developers to rewrite apps for every hardware', False),
                            ('Supported by Meta, Valve, HTC & Microsoft', True),
                            ('Is limited to a single proprietary ecosystem', False),
                        ]
                    },
                    {
                        'text': 'What is the XR Interaction Toolkit (XRI)?',
                        'choices': [
                            ('A component-based framework for handling spatial interactions', True),
                            ('A hardware device for VR headsets', False),
                            ('A graphics engine for 2D games', False),
                            ('A programming language for AR apps', False),
                        ]
                    },
                    {
                        'text': 'What core capability do ARCore and ARKit provide?',
                        'choices': [
                            ('Only 3D rendering', False),
                            ('Only multiplayer networking', False),
                            ('Visual-Inertial Odometry (VIO) for motion tracking and plane detection', True),
                            ('Hardware-level VR processing', False),
                        ]
                    },
                    {
                        'text': 'What does "Zero-Friction Access" mean in XR?',
                        'choices': [
                            ('Accessing content only via dedicated apps', False),
                            ('Using hardware controllers to interact', False),
                            ('Delivering immersive content directly through web browsers', True),
                            ('Requiring installation of heavy SDKs', False),
                        ]
                    },
                    {
                        'text': 'What is the main purpose of stereoscopic rendering in XR?',
                        'choices': [
                            ('Improve internet speed', False),
                            ('Create depth perception using two images', True),
                            ('Reduce battery consumption', False),
                            ('Detect objects in the environment', False),
                        ]
                    },
                    {
                        'text': 'What does spatial audio provide in XR environments?',
                        'choices': [
                            ('Faster graphics rendering', False),
                            ('Realistic sound direction and distance perception', True),
                            ('Higher screen resolution', False),
                            ('Improved internet connectivity', False),
                        ]
                    },
                    {
                        'text': 'Which rendering technique simulates how light interacts with objects to produce realistic reflections and shadows?',
                        'choices': [
                            ('Ray tracing', True),
                            ('Motion tracking', False),
                            ('Plane detection', False),
                            ('Object recognition', False),
                        ]
                    },
                    {
                        'text': 'What is the purpose of plane detection in spatial computing?',
                        'choices': [
                            ('To increase frame rate', False),
                            ('To detect flat surfaces like floors and tables', True),
                            ('To improve audio quality', False),
                            ('To reduce GPU usage', False),
                        ]
                    },
                    {
                        'text': 'What do spatial anchors allow XR systems to do?',
                        'choices': [
                            ('Improve internet speed', False),
                            ('Track eye movement', False),
                            ('Keep virtual objects fixed in the same real-world location', True),
                            ('Increase screen brightness', False),
                        ]
                    },
                ]
            },
            {
                'title': 'Principles of User Experience Design for XR',
                'questions': [
                    {
                        'text': 'Which technology adds digital objects to the real world without replacing it, like Pokémon GO?',
                        'choices': [
                            ('Augmented Reality (AR)', True),
                            ('Analog Reality', False),
                            ('Virtual Reality (VR)', False),
                            ('Static Reality', False),
                        ]
                    },
                    {
                        'text': 'Which interaction method allows users to select objects by looking at them?',
                        'choices': [
                            ('Gesture control', False),
                            ('Voice command', False),
                            ('Gaze-based interaction', True),
                            ('Controller tracking', False),
                        ]
                    },
                    {
                        'text': 'What is the primary goal of XR design that makes the brain believe the digital world is real?',
                        'choices': [
                            ('Fast Loading', False),
                            ('Color Contrast', False),
                            ('Sense of Presence', True),
                            ('High Resolution', False),
                        ]
                    },
                    {
                        'text': "Which type of UI is a natural part of the story or the 3D world, like a watch on a character's wrist?",
                        'choices': [
                            ('Non-Diegetic UI', False),
                            ('Diegetic UI', True),
                            ('Static UI', False),
                            ('Flat UI', False),
                        ]
                    },
                    {
                        'text': 'How does user interaction change when moving from 2D screens to Spatial Computing?',
                        'choices': [
                            ('From 3D to 2D', False),
                            ('Only Mouse Clicks', False),
                            ('More Keyboard', False),
                            ('From Clicking to Natural Gestures', True),
                        ]
                    },
                    {
                        'text': 'In XR, what is "Haptic Feedback"?',
                        'choices': [
                            ('A high-resolution 3D image.', False),
                            ('A physical vibration or sensation felt when touching a virtual object.', True),
                            ('A voice command used to control the headset.', False),
                            ('The speed of the internet connection.', False),
                        ]
                    },
                    {
                        'text': 'What is the main purpose of haptic feedback in XR environments?',
                        'choices': [
                            ('To improve visual quality', False),
                            ('To simulate the sense of touch', True),
                            ('To increase system speed', False),
                            ('To create 3D models', False),
                        ]
                    },
                    {
                        'text': 'What does spatial audio help users understand in XR environments?',
                        'choices': [
                            ('The color of objects', False),
                            ('The brightness of the screen', False),
                            ('The size of virtual objects', False),
                            ('The direction and location of sounds', True),
                        ]
                    },
                    {
                        'text': 'Which input method allows users to control virtual objects using hand movements?',
                        'choices': [
                            ('Gesture control', True),
                            ('Eye tracking', False),
                            ('Voice commands', False),
                            ('Spatial audio', False),
                        ]
                    },
                    {
                        'text': 'What is one key goal of natural interaction in XR design?',
                        'choices': [
                            ('Making systems more complex', False),
                            ('Increasing hardware requirements', False),
                            ('Making interaction similar to real-world actions', True),
                            ('Removing all input methods', False),
                        ]
                    },
                    {
                        'text': 'What causes "Vergence-Accommodation Conflict" in XR?',
                        'choices': [
                            ('Slow internet speed', False),
                            ('High device price', False),
                            ('Focus-depth mismatch', True),
                            ('Battery overheating', False),
                        ]
                    },
                    {
                        'text': 'What is the main goal of the "Prototyping Loop"?',
                        'choices': [
                            ('Testing button ergonomics', True),
                            ('Writing final code', False),
                            ('Marketing the app', False),
                            ('Choosing font colors', False),
                        ]
                    },
                    {
                        'text': 'In the future, what will "Contextual AI" do?',
                        'choices': [
                            ('Play random music', False),
                            ('Delete user data', False),
                            ('Increase screen brightness', False),
                            ('Identify broken appliances', True),
                        ]
                    },
                    {
                        'text': 'How is "360° Storyboarding" different from 2D UI?',
                        'choices': [
                            ('It uses fewer colors', False),
                            ('It maps the environment', True),
                            ('It is only for mobile', False),
                            ('It requires no design', False),
                        ]
                    },
                    {
                        'text': 'What does "Remote Assistance" allow experts to do?',
                        'choices': [
                            ('Draw 3D instructions in AR', True),
                            ("Control the technician's hands", False),
                            ("Record the technician's voice", False),
                            ("Pay the technician's salary", False),
                        ]
                    },
                    {
                        'text': 'What does "The Body is the Interface" mean in XR?',
                        'choices': [
                            ('Using a keyboard and mouse to control the virtual world.', False),
                            ('Use physical movements as the primary way to interact with digital content', True),
                            ('Only using hand controllers to click on buttons.', False),
                            ('Watching a 3D movie without moving at all.', False),
                        ]
                    },
                    {
                        'text': 'What is the main cause of "Cyber-sickness"?',
                        'choices': [
                            ('The headset being too heavy on the user\'s head.', False),
                            ('Conflict between the motion seen by the eyes and the stillness felt by body', True),
                            ('Using colors that are too bright in the application.', False),
                            ('Looking at objects that are very far away.', False),
                        ]
                    },
                    {
                        'text': 'How can designers prevent "Gorilla Arm" syndrome?',
                        'choices': [
                            ('By placing buttons at chest or waist level, users can keep their arms comfortable.', True),
                            ('By making the virtual buttons much larger.', False),
                            ('By asking the user to take a break every five minutes.', False),
                            ('By forcing users to use both hands at the same time.', False),
                        ]
                    },
                    {
                        'text': 'Why is the "Sweet Spot" (central 30-degree cone) important?',
                        'choices': [
                            ('It makes the colors look more realistic.', False),
                            ('Ensures crucial content is placed where eyes see clearly without neck strain', True),
                            ('It helps the headset battery last longer.', False),
                            ('It allows more people to watch the screen.', False),
                        ]
                    },
                    {
                        'text': 'What is the purpose of a "Virtual Floor" or grid in XR?',
                        'choices': [
                            ('To make the game look more futuristic.', False),
                            ('To show where the user can find hidden items.', False),
                            ('To give the user a sense of stability and help the brain reduce dizziness.', True),
                            ("To hide mistakes in the environment's graphics.", False),
                        ]
                    },
                    {
                        'text': 'What is the main goal of good XR UX design?',
                        'choices': [
                            ('Only focus on graphics', False),
                            ('Make users dizzy', False),
                            ('Engage users safely and comfortably', True),
                            ('Display all menus constantly', False),
                        ]
                    },
                    {
                        'text': 'What is a common mistake in XR design?',
                        'choices': [
                            ('Minimalist interface', False),
                            ('Crowded interface with too much info', True),
                            ('Step-by-step onboarding', False),
                            ('Comfortable viewing distance', False),
                        ]
                    },
                    {
                        'text': 'How can XR help workers in factories?',
                        'choices': [
                            ('By providing step-by-step AR instructions', True),
                            ('By playing music', False),
                            ('By reducing salaries', False),
                            ('By only using VR games', False),
                        ]
                    },
                    {
                        'text': 'What role does spatial audio play in XR?',
                        'choices': [
                            ('Reduces file size', False),
                            ('Makes sounds come from directions', True),
                            ('Increases battery life', False),
                            ('Improves color contrast', False),
                        ]
                    },
                    {
                        'text': 'Which movement option helps users feel comfortable in XR?',
                        'choices': [
                            ('Teleportation', True),
                            ('Fast spinning', False),
                            ('Invisible walking', False),
                            ('Random jumping', False),
                        ]
                    },
                    {
                        'text': 'Why is onboarding important in XR?',
                        'choices': [
                            ('It teaches users how to interact safely', True),
                            ('It makes graphics faster', False),
                            ('It increases sound volume', False),
                            ('It reduces battery use', False),
                        ]
                    },
                    {
                        'text': 'What is the purpose of privacy indicators like small LEDs in XR devices?',
                        'choices': [
                            ('Make devices look cool', False),
                            ('Show battery level', False),
                            ('Inform when camera is recording', True),
                            ('Increase frame rate', False),
                        ]
                    },
                    {
                        'text': 'Which interaction is NOT common in XR?',
                        'choices': [
                            ('Hand gestures', False),
                            ('Voice commands', False),
                            ('Physical buttons', False),
                            ('Only keyboard typing', True),
                        ]
                    },
                    {
                        'text': 'How can XR systems reduce distractions?',
                        'choices': [
                            ('Fill the field of view with menus', False),
                            ('Use very strong sounds', False),
                            ('Keep interface minimal and subtle', True),
                            ('Avoid onboarding', False),
                        ]
                    },
                    {
                        'text': 'In XR, what is the principle of "Minimalism"?',
                        'choices': [
                            ('Use bright colors everywhere', False),
                            ('Display interface only when necessary', True),
                            ('Include many menus', False),
                            ('Avoid physical buttons', False),
                        ]
                    },
                    {
                        'text': 'Which design problem can cause motion sickness?',
                        'choices': [
                            ('Smooth animations', False),
                            ('Minimal interfaces', False),
                            ('Simple colors', False),
                            ('Fast camera movements', True),
                        ]
                    },
                    {
                        'text': 'What should AR designers consider when users interact with AR in different environments?',
                        'choices': [
                            ('Screen brightness only', False),
                            ('Environmental conditions (light, space, noise)', True),
                            ('Avatar clothing design', False),
                            ('Background music', False),
                        ]
                    },
                    {
                        'text': 'Which principle helps users avoid physical fatigue in XR?',
                        'choices': [
                            ('Environmental adaptation', False),
                            ('Physical comfort', True),
                            ('Motion sickness prevention', False),
                            ('Minimalism', False),
                        ]
                    },
                    {
                        'text': 'How is XR UX different from traditional 2D UX?',
                        'choices': [
                            ('It is designed for three-dimensional space', True),
                            ('It uses bigger buttons', False),
                            ('It does not need testing', False),
                            ('Users only click with a mouse', False),
                        ]
                    },
                    {
                        'text': 'What is a common physical problem caused by bad XR design?',
                        'choices': [
                            ('Headaches', True),
                            ('Finger cramps', False),
                            ('Hair loss', False),
                            ('Sweating', False),
                        ]
                    },
                    {
                        'text': 'Why is UX important in XR?',
                        'choices': [
                            ('It improves battery life', False),
                            ('Poor design can cause motion sickness', True),
                            ('It makes apps load faster', False),
                            ('Users prefer bright colors', False),
                        ]
                    },
                    {
                        'text': 'In which XR type can digital objects interact with the real world?',
                        'choices': [
                            ('Virtual Reality', False),
                            ('Mixed Reality', True),
                            ('Augmented Reality', False),
                            ('2D Apps', False),
                        ]
                    },
                    {
                        'text': 'What is one way XR can increase user motivation and confidence?',
                        'choices': [
                            ('Adding more menus', False),
                            ('Using very bright colors', False),
                            ('Creating small moments of success', True),
                            ('Filling the entire field of view', False),
                        ]
                    },
                    {
                        'text': 'Why should frequently used XR menus be placed at "easy reach" distance?',
                        'choices': [
                            ('To reduce physical fatigue', True),
                            ('To improve graphics', False),
                            ('To prevent privacy leaks', False),
                            ('To save battery', False),
                        ]
                    },
                    {
                        'text': 'Which XR design principle helps users stay aware of real-world objects while using XR?',
                        'choices': [
                            ('Motion speed control', False),
                            ('Spatial awareness and safe interaction', True),
                            ('Color theme design', False),
                            ('Avatar customization', False),
                        ]
                    },
                ]
            },
            {
                'title': 'Use of XR in Industries',
                'questions': [
                    {
                        'text': 'What does Extended Reality (XR) encompass?',
                        'choices': [
                            ('Immersive tech for physical and digital realms', True),
                            ('A program purely for playing modern video games at home', False),
                            ('Software to modify or edit a basic video file', False),
                            ('Basic phone interfaces for browsing the internet', False),
                        ]
                    },
                    {
                        'text': 'What is the main difference between Virtual Reality (VR) and Augmented Reality (AR)?',
                        'choices': [
                            ('AR blocks the real world, VR enhances it', False),
                            ('VR entirely replaces reality; AR overlays digital parts onto your true view', True),
                            ('VR is for phones, AR is for a visor', False),
                            ('VR uses physical items, AR uses a display', False),
                        ]
                    },
                    {
                        'text': 'What is the projected market value of the XR industry by 2032?',
                        'choices': [
                            ('Exactly an amount close to two grand', False),
                            ('Over a huge amount near five thousand units by 2050', False),
                            ('Around five hundred big units', False),
                            ('Approaching 1.6 trillion dollars by 2032', True),
                        ]
                    },
                    {
                        'text': 'According to the presentation, what is a major business benefit of XR?',
                        'choices': [
                            ('Extra travel prices for workers who have to fly far for group chat', False),
                            ('Effectively reducing training costs and risk', True),
                            ('Slower manufacturing times in the plant', False),
                            ('Higher reliance on physical prototypes', False),
                        ]
                    },
                    {
                        'text': 'How is XR transforming surgical training in healthcare?',
                        'choices': [
                            ('It makes operating on humans very expensive', False),
                            ('It provides basic instructions on a display', False),
                            ('It replaces the requirement for human doctors', False),
                            ('It lets surgeons practice complex procedures safely in a detailed virtual 3D environment', True),
                        ]
                    },
                    {
                        'text': 'How does VR help with patient pain management?',
                        'choices': [
                            ('Successfully distracting minds from pain', True),
                            ('Curing the major disease right away', False),
                            ('Delivering physical medicine via complex robotic machines', False),
                            ('Elevating the heart rate to fight pain', False),
                        ]
                    },
                    {
                        'text': 'What is one practical use of Augmented Reality (AR) in the operating room?',
                        'choices': [
                            ('Playing relaxing tracks to calm the patient down', False),
                            ('Assisting surgeons by overlaying vital data', True),
                            ('Exchanging surgical instruments for digital ones', False),
                            ('Lowering the lights in the surgery area', False),
                        ]
                    },
                    {
                        'text': 'In manufacturing, what problem does XR primarily solve?',
                        'choices': [
                            ('Addressing the high cost of complex training', True),
                            ('The lack of a steady signal in remote plants', False),
                            ('The demand for huge physical storage areas', False),
                            ('A high number of workers taking a break at once', False),
                        ]
                    },
                    {
                        'text': 'What is a "Digital Twin" in the context of manufacturing?',
                        'choices': [
                            ('A backup worker for a machine operator', False),
                            ('A virtual replica of a physical object or system to simulate prior to launch', True),
                            ('A 3D printer that creates matched parts', False),
                            ('A second physical factory built nearby', False),
                        ]
                    },
                    {
                        'text': 'How does AR assist with remote maintenance on a factory floor?',
                        'choices': [
                            ('Shutting down the plant by itself if broken', False),
                            ('Making industrial machines operate by themselves with zero human oversight', False),
                            ('Allowing off-site experts to guide in real time', True),
                            ('Buying spare parts from the web via a catalog', False),
                        ]
                    },
                    {
                        'text': 'How are automotive brands using XR to improve the customer experience?',
                        'choices': [
                            ('Forcing customers to wear heavy visors to buy a car', False),
                            ('Sending physical cars to a client home', False),
                            ('Replacing human salespeople with AI bots', False),
                            ('Offering virtual showrooms to test drive cars', True),
                        ]
                    },
                    {
                        'text': 'What is the learning retention rate for immersive VR training compared to traditional reading?',
                        'choices': [
                            ('Plunging to a mere 5% due to digital diversions', False),
                            ('Attaining up to 75% retention versus 10%', True),
                            ('Exactly like reading an educational document in a quiet place', False),
                            ('Around 20% higher than standard lectures', False),
                        ]
                    },
                    {
                        'text': "How did Macy's benefit from using AR product visualization?",
                        'choices': [
                            ('By allowing a virtual try-before-you-buy, they cut return rates under 2%', True),
                            ('They stopped selling physical furniture entirely', False),
                            ('They gained a huge number of new social media fans', False),
                            ('They created fifty new physical retail shops', False),
                        ]
                    },
                    {
                        'text': 'What is a popular application of XR in the real estate industry?',
                        'choices': [
                            ('Arranging virtual tours and furnishing spaces', True),
                            ('Removing the requirement for real estate agents', False),
                            ('Altering the physical location of a house', False),
                            ('Building houses using huge 3D printers', False),
                        ]
                    },
                    {
                        'text': 'Which of the following is cited as a major challenge for XR adoption?',
                        'choices': [
                            ('The tech is beyond fragile and breaks easily during factory operations', False),
                            ('Bottlenecks in content creation and high costs', True),
                            ('Every single person on earth already owns a visor', False),
                            ('There are zero privacy concerns in any way', False),
                        ]
                    },
                    {
                        'text': 'What health concern is associated with prolonged use of VR headsets?',
                        'choices': [
                            ('A giant spike in your daily physical strength', False),
                            ('A permanent wipe of your basic digital memory', False),
                            ('A huge reduction in your basic hearing abilities', False),
                            ('Users can face motion sickness, eye strain, or headaches from VR use', True),
                        ]
                    },
                    {
                        'text': 'What role will 5G play in the future of XR?',
                        'choices': [
                            ('Making visors heavier and more expensive due to huge physical wires', False),
                            ('Removing the requirement for any electricity', False),
                            ('Limiting XR to only local, wired format', False),
                            ('Connecting devices with low latency for the cloud', True),
                        ]
                    },
                    {
                        'text': 'How is Artificial Intelligence improving XR environments?',
                        'choices': [
                            ('Supplying smart features like object tracking', True),
                            ('Erasing user data without asking first', False),
                            ('Making the simulations show up more pixelated', False),
                            ('Preventing users from moving in space by locking visors into a spot', False),
                        ]
                    },
                    {
                        'text': 'How is generative AI expected to impact XR content creation?',
                        'choices': [
                            ('It can replace hardware creation entirely', False),
                            ('It can only be used for typing text', False),
                            ('AI can generate 3D models and virtual spaces to save both time and money', True),
                            ('It can make XR content very hard to modify', False),
                        ]
                    },
                    {
                        'text': 'What is spatial computing?',
                        'choices': [
                            ('Using keyboards instead of touch display devices', False),
                            ('Accurately mapping computers to physical space', True),
                            ('Storing data on orbiters in outer space', False),
                            ('Measuring the physical distance from two displays using a digital ruler', False),
                        ]
                    },
                ]
            },
            {
                'title': 'Use of AI in Art & Music, Healthcare: Opportunities & Challenges',
                'questions': [
                    {
                        'text': 'Which of the following is a type of AI?',
                        'choices': [
                            ('Machine Learning', True),
                            ('Web Design', False),
                            ('Photoshop', False),
                            ('Hardware', False),
                        ]
                    },
                    {
                        'text': 'What is Deep Learning?',
                        'choices': [
                            ('A simple data storage system', False),
                            ('A more complex AI learning model', True),
                            ('A type of robot', False),
                            ('A programming language', False),
                        ]
                    },
                    {
                        'text': 'Which field uses AI for disease diagnosis?',
                        'choices': [
                            ('Finance', False),
                            ('Entertainment', False),
                            ('Healthcare', True),
                            ('Agriculture', False),
                        ]
                    },
                    {
                        'text': 'What can AI do in art?',
                        'choices': [
                            ('Only copy existing art', False),
                            ('Create new artworks using data', True),
                            ('Destroy paintings', False),
                            ('Print books', False),
                        ]
                    },
                    {
                        'text': 'Which tool is used to generate images with AI?',
                        'choices': [
                            ('Excel', False),
                            ('DALL·E', True),
                            ('Word', False),
                            ('Chrome', False),
                        ]
                    },
                    {
                        'text': 'What is one benefit of AI in music?',
                        'choices': [
                            ('Slower production', False),
                            ('Higher costs', False),
                            ('Faster music production', True),
                            ('Less creativity', False),
                        ]
                    },
                    {
                        'text': 'What is a major concern about AI-generated music?',
                        'choices': [
                            ('It is too loud', False),
                            ('Copyright issues', True),
                            ('It uses too much electricity', False),
                            ('It cannot be saved', False),
                        ]
                    },
                    {
                        'text': 'How does AI help in healthcare?',
                        'choices': [
                            ('By replacing doctors completely', False),
                            ('By supporting diagnosis and treatment', True),
                            ('By building hospitals', False),
                            ('By selling medicine', False),
                        ]
                    },
                    {
                        'text': 'What is one challenge of AI in healthcare?',
                        'choices': [
                            ('Too many doctors', False),
                            ('Data privacy risks', True),
                            ('No internet', False),
                            ('Too much paper', False),
                        ]
                    },
                    {
                        'text': 'Why is AI important today?',
                        'choices': [
                            ('It is only used in games', False),
                            ('It creates major changes in many fields', True),
                            ('It replaces electricity', False),
                            ('It only stores data', False),
                        ]
                    },
                    {
                        'text': 'How does VR help patients during painful or long medical treatments (like chemotherapy)?',
                        'choices': [
                            ('It cures their disease completely.', False),
                            ('It makes them fall asleep instantly.', False),
                            ('It provides a mental escape and distracts them from pain.', True),
                            ('It changes the temperature of the hospital room.', False),
                        ]
                    },
                    {
                        'text': 'What is the main goal of "Therapeutic Exposure" in XR?',
                        'choices': [
                            ('To safely help patients face and overcome their fears.', True),
                            ('To teach doctors how to perform surgery.', False),
                            ("To scan a patient's brain.", False),
                            ('To test new medical drugs.', False),
                        ]
                    },
                    {
                        'text': 'Why is XR 3D Visualization better than traditional learning for medical students?',
                        'choices': [
                            ("They don't need to read any books anymore.", False),
                            ('It lets them interact with 3D organs instead of flat 2D pictures.', True),
                            ('It automatically takes their exams for them.', False),
                            ('It makes them surgeons in just one day.', False),
                        ]
                    },
                    {
                        'text': 'What does a "low-stakes environment" mean in VR medical training?',
                        'choices': [
                            ('A real surgery with a very high risk of failure.', False),
                            ('A cheap hospital room for low-income patients.', False),
                            ('A waiting room where doctors relax.', False),
                            ('A safe, virtual space where making mistakes is okay and part of learning.', True),
                        ]
                    },
                    {
                        'text': 'How does XR improve physical therapy for stroke patients?',
                        'choices': [
                            ('By turning boring, repetitive exercises into fun, interactive games.', True),
                            ('By doing the physical movements for them.', False),
                            ('By letting them rest in bed all day.', False),
                            ('By immediately healing their muscles.', False),
                        ]
                    },
                    {
                        'text': 'What is the biggest advantage of a surgeon using VR before a real, risky surgery?',
                        'choices': [
                            ('They can listen to a relaxing podcast during the operation.', False),
                            ('They can practice on a 3D model of the exact patient to minimize errors.', True),
                            ('They can operate without needing any nurses.', False),
                            ('They can live-stream the surgery on the internet.', False),
                        ]
                    },
                    {
                        'text': 'Who owns the copyright of a painting created 100% by AI?',
                        'choices': [
                            ('The AI software', False),
                            ('The person who wrote the prompt', False),
                            ('No one (Currently)', True),
                            ('The original artists', False),
                        ]
                    },
                    {
                        'text': 'Why did Spotify remove the song "Heart on My Sleeve"?',
                        'choices': [
                            ('It was too long', False),
                            ('It used voices without permission', True),
                            ('The music was bad', False),
                            ('It was a secret track', False),
                        ]
                    },
                    {
                        'text': 'What is "Algorithmic Bias" in healthcare?',
                        'choices': [
                            ('AI working too fast', False),
                            ('AI making unfair or racist decisions', True),
                            ('AI being too expensive', False),
                            ('AI saving too many lives', False),
                        ]
                    },
                    {
                        'text': 'If a robotic surgeon makes a mistake, who is legally responsible?',
                        'choices': [
                            ('The Robot', False),
                            ('The Software Company', False),
                            ('The Human Doctor', True),
                            ('No one', False),
                        ]
                    },
                    {
                        'text': "What is the name of the world's first major AI law?",
                        'choices': [
                            ('AI Freedom Act', False),
                            ('EU AI Act', True),
                            ('Global Robot Law', False),
                            ('Internet Safety Bill', False),
                        ]
                    },
                    {
                        'text': 'According to UNESCO 2026, which group faces a 24% income drop?',
                        'choices': [
                            ('Doctors', False),
                            ('Lawyers', False),
                            ('Music Producers', True),
                            ('Engineers', False),
                        ]
                    },
                    {
                        'text': 'Which of these is BANNED by the new AI laws?',
                        'choices': [
                            ('Making AI art', False),
                            ('Social Scoring of people', True),
                            ('Playing chess with AI', False),
                            ('Writing emails with AI', False),
                        ]
                    },
                    {
                        'text': 'What is the biggest advantage of new AI tools in 3D world generation?',
                        'choices': [
                            ('They only create black and white models.', False),
                            ('They build physics-aware 3D objects in seconds.', True),
                            ('They require weeks of manual coding.', False),
                            ('They remove digital gravity completely.', False),
                        ]
                    },
                    {
                        'text': 'How do AI-powered virtual art galleries differ from traditional ones?',
                        'choices': [
                            ('They display static, unchanging paintings.', False),
                            ('They actively react to audience movements and lighting.', True),
                            ('They can only be viewed on a mobile phone.', False),
                            ('They delete artworks after 24 hours.', False),
                        ]
                    },
                    {
                        'text': 'What makes AI World Models unique?',
                        'choices': [
                            ('They turn simple text into fully playable 3D universes.', True),
                            ('They only generate 2D silent videos.', False),
                            ('They block users from moving around.', False),
                            ('They design simple avatars for games.', False),
                        ]
                    },
                    {
                        'text': 'What is the main function of scene-aware AI acoustics in VR?',
                        'choices': [
                            ('To mute all background noise in games.', False),
                            ('To instantly calculate realistic room echoes.', True),
                            ('To translate the user voice instantly.', False),
                            ('To play repeating, pre-recorded music loops.', False),
                        ]
                    },
                    {
                        'text': 'What data do biometric AI music engines use to change the soundtrack?',
                        'choices': [
                            ('The user internet connection speed.', False),
                            ('Real-time heart rate and eye movements.', True),
                            ('A randomly generated playlist.', False),
                            ('The battery level of the VR headset.', False),
                        ]
                    },
                ]
            },
        ]

        total_added = 0
        for session_data in sessions_data:
            session_title = session_data['title']
            session_slug = slugify(session_title)
            session, created = Session.objects.get_or_create(
                course=course,
                slug=session_slug,
                defaults={'title': session_title, 'is_published': True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created session: {session_title}'))
            else:
                self.stdout.write(f'  Using existing session: {session_title}')

            existing_count = session.questions.count()
            if existing_count > 0:
                self.stdout.write(f'  Skipping — already has {existing_count} questions.')
                continue

            for order, q_data in enumerate(session_data['questions'], start=1):
                question = Question.objects.create(
                    session=session,
                    text=q_data['text'],
                    order=order,
                    is_active=True,
                )
                for choice_text, is_correct in q_data['choices']:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct,
                    )
                total_added += 1

            self.stdout.write(self.style.SUCCESS(f'  Added {len(session_data["questions"])} questions.'))

        self.stdout.write(self.style.SUCCESS(f'\nDone. Total questions added: {total_added}'))
