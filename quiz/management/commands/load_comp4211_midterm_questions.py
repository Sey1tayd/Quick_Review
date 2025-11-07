from django.core.management.base import BaseCommand
from quiz.models import Course, Session, Question, Choice


class Command(BaseCommand):
    help = 'Load COMP4211 Blockchain Technology and Applications Midterm questions into the database'

    def handle(self, *args, **options):
        # Create or get course
        course, created = Course.objects.get_or_create(
            slug='COMP4211',
            defaults={
                'title': 'COMP4211 Blockchain Technology and Applications',
                'description': 'Blockchain Technology course covering consensus mechanisms, smart contracts, cryptography, distributed systems, and DApp development.'
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

        # All questions for COMP4211 Midterm
        questions = [
            {
                'text': 'Which trio constitutes the well-known "blockchain trilemma" that systems strive to balance?',
                'choices': [
                    ('Throughput, Fees, Governance', False),
                    ('Scalability, Security, Decentralization', True),
                    ('Privacy, Compliance, Interoperability', False),
                    ('Latency, Bandwidth, Consistency', False),
                ],
                'feedback': 'Designs typically optimize two of Scalability, Security, and Decentralization, trading off the third.'
            },
            {
                'text': 'Which property of hash functions means it is hard to find any two different inputs with the same output?',
                'choices': [
                    ('Avalanche effect', False),
                    ('Preimage resistance', False),
                    ('Collision resistance', True),
                    ('Second preimage resistance', False),
                ],
                'feedback': 'Collision resistance ensures it is hard to find any x ≠ x\' with h(x) = h(x\').'
            },
            {
                'text': 'In PBFT with n replicas, what bound on Byzantine faults f is tolerated to maintain safety and liveness?',
                'choices': [
                    ('f < n/3', True),
                    ('f < n/4', False),
                    ('f < n/2', False),
                    ('f < 2n/3', False),
                ],
                'feedback': 'PBFT requires n = 3f + 1, so it tolerates strictly less than n/3 Byzantine replicas.'
            },
            {
                'text': 'Which statement about protocol forks is accurate?',
                'choices': [
                    ('Both soft and hard forks always require unanimous node upgrades.', False),
                    ('A soft fork tightens rules (narrower valid set), while a hard fork loosens rules (wider valid set).', True),
                    ('A soft fork expands valid blocks, a hard fork narrows them.', False),
                    ('Only hard forks can be activated via miner signaling.', False),
                ],
                'feedback': 'A soft fork narrows the set of valid blocks/transactions and is backward-compatible for non-upgraded nodes; a hard fork expands validity and requires coordinated upgrades.'
            },
            {
                'text': 'Which description best characterizes the Unspent Transaction Output (UTXO) model used by some blockchains?',
                'choices': [
                    ('State is a set of unspent outputs; transactions consume previous outputs as inputs and create new outputs.', True),
                    ('A global mapping of address → (balance, nonce, code, storage) mutated by transactions.', False),
                    ('Only a single shared ledger balance plus a transaction counter.', False),
                    ('An off-chain database of user balances periodically reconciled on-chain.', False),
                ],
                'feedback': 'In the UTXO model, state is the set of unspent outputs; transactions consume prior outputs and create new ones.'
            },
            {
                'text': 'Which one of the following actions performed from a DApp frontend typically requires the user to pay a gas fee?',
                'choices': [
                    ('Getting the current block number from the provider.', False),
                    ('Calling a function that transfers an NFT from one user to another.', True),
                    ('Reading the symbol() of an ERC-20 token contract.', False),
                    ('Calling a view function to check the balance of a specific token for an address.', False),
                ],
                'feedback': 'Gas fees are required for operations that change the state of the blockchain (write operations). Read-only operations like view functions are free.'
            },
            {
                'text': 'What is the primary security purpose of including a Chain ID when signing a transaction?',
                'choices': [
                    ('To determine the amount of gas the transaction will consume.', False),
                    ('To serve as the unique identifier for the transaction itself.', False),
                    ('To specify which block the transaction should be included in.', False),
                    ('To prevent transaction replay attacks across different blockchain networks.', True),
                ],
                'feedback': 'The Chain ID (defined in EIP-155) ensures that a transaction intended for one network cannot be maliciously rebroadcast on another network.'
            },
            {
                'text': 'How often does the Bitcoin network adjust its mining difficulty target?',
                'choices': [
                    ('Every block', False),
                    ('Every 210,000 blocks', False),
                    ('Every 2016 blocks', True),
                    ('Every 144 blocks', False),
                ],
                'feedback': 'The network retargets difficulty every 2016 blocks, roughly every two weeks on average.'
            },
            {
                'text': 'In Proof of Work systems, which chain selection rule is commonly used to resolve competing forks?',
                'choices': [
                    ('Choose the chain with the most nodes connected to it', False),
                    ('Choose the valid chain with the greatest cumulative proof of work', True),
                    ('Choose the chain with the highest average fee', False),
                    ('Choose the chain proposed by the oldest node', False),
                ],
                'feedback': 'Nodes adopt the valid chain with the greatest cumulative PoW (often called the longest chain rule).'
            },
            {
                'text': 'What is the primary role of a smart contract within the architecture of a Decentralized Application (DApp)?',
                'choices': [
                    ('To provide a reliable connection to a blockchain node via a URL.', False),
                    ('To render the user interface and handle user clicks.', False),
                    ('To execute the application\'s backend logic and manage its state on the blockchain.', True),
                    ('To securely store the user\'s private keys and sign transactions.', False),
                ],
                'feedback': 'In a DApp, the smart contract functions as the backend. It contains the business logic, defines the rules, and manages the application\'s state on the decentralized blockchain network.'
            },
            {
                'text': 'Which of the following EVM data locations is the MOST expensive in terms of gas consumption?',
                'choices': [
                    ('Calldata', False),
                    ('Memory', False),
                    ('Storage', True),
                    ('Stack', False),
                ],
                'feedback': 'Storage is the most expensive data location because it persists on the blockchain permanently. Writing to storage (SSTORE operation) can cost over 20,000 gas.'
            },
            {
                'text': 'What value is returned when you access a non-existent key in a Solidity mapping of type mapping(address => uint256)?',
                'choices': [
                    ('The default value (0 for uint256)', True),
                    ('undefined', False),
                    ('An error is thrown', False),
                    ('null', False),
                ],
                'feedback': 'Mappings return the default value for the value type when a key doesn\'t exist. For uint256, the default value is 0.'
            },
            {
                'text': 'Under a fee mechanism with a protocol base fee and a user-specified max fee and priority fee, the per-unit effective gas price the user pays is min(max_fee, base_fee + priority_fee).',
                'choices': [
                    ('True', True),
                    ('False', False),
                ],
                'feedback': 'With base fee burned and tip paid to the block producer, the user\'s effective gas price is min(max_fee, base_fee + priority_fee). Total cost is this price times gas used.'
            },
            {
                'text': 'Delegated Proof-of-Stake achieves high throughput primarily by making which trade-off?',
                'choices': [
                    ('Eliminating any form of governance or voting.', False),
                    ('Sacrificing fast finality for probabilistic confirmation.', False),
                    ('Reduced decentralization via a small set of elected delegates.', True),
                    ('Significantly increased energy consumption.', False),
                ],
                'feedback': 'DPoS concentrates block production in a small, elected set of delegates, reducing decentralization.'
            },
            {
                'text': 'Which consensus mechanism is typically favored for consortium/permissioned networks with known identities and a need for deterministic finality?',
                'choices': [
                    ('PBFT (Practical Byzantine Fault Tolerance)', True),
                    ('PoW (Proof-of-Work)', False),
                    ('PoS with longest-chain selection only', False),
                    ('Proof-of-History as a standalone mechanism', False),
                ],
                'feedback': 'PBFT-style protocols provide deterministic finality and strong safety under f < n/3, fitting controlled membership.'
            },
            {
                'text': 'Who is the instructor for COMP4211 Blockchain Technology and Applications?',
                'choices': [
                    ('Dr. Yusuf Kursat Tuncel', True),
                    ('Dr. Andreas Antonopoulos', False),
                    ('Dr. Vitalik Buterin', False),
                    ('Dr. Satoshi Nakamoto', False),
                ],
                'feedback': 'The instructor is Dr. Yusuf Kursat Tuncel.'
            },
            {
                'text': 'To tolerate up to f Byzantine faults, what is the minimum number of nodes required in a classical BFT setting?',
                'choices': [
                    ('f + 1', False),
                    ('2f + 1', False),
                    ('4f', False),
                    ('3f + 1', True),
                ],
                'feedback': 'Classical BFT requires at least 3f + 1 replicas to tolerate f Byzantine faults.'
            },
            {
                'text': 'Reusing nonces in ECDSA can leak the secret key.',
                'choices': [
                    ('True', True),
                    ('False', False),
                ],
                'feedback': 'Yes, reusing nonces in ECDSA is catastrophic and can leak the secret key.'
            },
            {
                'text': 'Which statement best describes a core limitation of Proof-of-Work in permissionless blockchains?',
                'choices': [
                    ('It consumes large amounts of energy and typically achieves low transactions per second.', True),
                    ('It eliminates centralization pressures by preventing mining pools.', False),
                    ('It does not require economic incentives for security.', False),
                    ('It provides deterministic finality for every block by design.', False),
                ],
                'feedback': 'PoW secures open networks but is energy-intensive and offers modest throughput.'
            },
            {
                'text': 'Which curve is the Bitcoin standard for ECDSA?',
                'choices': [
                    ('secp256r1', False),
                    ('Curve25519', False),
                    ('Ed25519', False),
                    ('secp256k1', True),
                ],
                'feedback': 'The Bitcoin standard uses secp256k1.'
            },
            {
                'text': 'In an account-based blockchain, what is the primary purpose of maintaining a per-account nonce?',
                'choices': [
                    ('To determine transaction fees dynamically from network load.', False),
                    ('To prevent replay and enforce per-account transaction ordering.', True),
                    ('To store contract bytecode size for execution limits.', False),
                    ('To compute the Merkle inclusion proof length.', False),
                ],
                'feedback': 'Nonces provide replay protection and enforce transaction ordering per account by requiring strictly increasing sequence numbers.'
            },
            {
                'text': 'What is the primary purpose of a contract\'s Application Binary Interface (ABI) in a frontend application?',
                'choices': [
                    ('To provide a machine-readable description of the contract\'s functions and events, enabling the frontend to format transactions correctly.', True),
                    ('It contains the compiled EVM bytecode that is deployed on the blockchain.', False),
                    ('To store the private keys required to deploy the contract.', False),
                    ('To define the visual layout and styling of the DApp\'s user interface.', False),
                ],
                'feedback': 'The ABI acts as a bridge between human-readable code and machine-readable bytecode. It\'s a JSON file that describes a contract\'s functions and events.'
            },
            {
                'text': 'The course COMP4211 is worth 6 ECTS credits.',
                'choices': [
                    ('True', True),
                    ('False', False),
                ],
                'feedback': 'Yes, it is 6 ECTS with 3+0 hours.'
            },
            {
                'text': 'What mechanism most directly mitigates the "nothing-at-stake" issue in Proof-of-Stake networks?',
                'choices': [
                    ('Increasing block gas limits.', False),
                    ('Shortening block intervals.', False),
                    ('Slashing validators that sign conflicting chains.', True),
                    ('Using ASIC-resistant hashing algorithms.', False),
                ],
                'feedback': 'Slashing economically penalizes validators for equivocation (e.g., signing conflicting chains), aligning incentives with honest behavior.'
            },
            {
                'text': 'In a blockchain that commits transactions via a Merkle root, the complexity of a Simple Payment Verification (SPV) inclusion proof for one transaction among n is:',
                'choices': [
                    ('O(n log n)', False),
                    ('O(1)', False),
                    ('O(log n)', True),
                    ('O(n)', False),
                ],
                'feedback': 'SPV proofs use Merkle paths of length proportional to log n, requiring a logarithmic number of hashes.'
            },
            {
                'text': 'Why is it considered a critical security failure to embed a user\'s private key directly into a DApp\'s frontend JavaScript code?',
                'choices': [
                    ('Because private keys are too long and would make the JavaScript file size too large.', False),
                    ('Because the frontend code is publicly visible, and anyone could read the key and steal the user\'s funds.', True),
                    ('Because JavaScript libraries like Ethers.js do not have functions that accept private keys.', False),
                    ('Because it violates the JSON-RPC specification for sending transactions.', False),
                ],
                'feedback': 'Frontend code is delivered to the user\'s browser and is therefore completely public. Embedding a private key would expose it to anyone who inspects the page.'
            },
            {
                'text': 'In the Ethers.js library, which object abstraction represents a read-only connection to the blockchain, suitable for fetching data but not for sending transactions?',
                'choices': [
                    ('Wallet', False),
                    ('Provider', True),
                    ('Signer', False),
                    ('Contract', False),
                ],
                'feedback': 'A Provider offers a read-only connection to the blockchain for fetching state, while a Signer can also sign and send transactions.'
            },
            {
                'text': 'A Merkle proof for a tree with n leaves is O(n) in size.',
                'choices': [
                    ('True', False),
                    ('False', True),
                ],
                'feedback': 'No, it is O(log n). Merkle proofs are logarithmic in size, not linear.'
            },
            {
                'text': 'In a proof-of-stake system, what is the purpose of slashing and how is finality typically achieved?',
                'choices': [
                    ('Slashing only delays payouts; finality depends on accumulating CPU work.', False),
                    ('Slashing deters/damages misbehavior by burning stake; finality arises from supermajority attestations over checkpoints.', True),
                    ('Slashing rewards inactivity; finality is purely probabilistic with no checkpoints.', False),
                    ('Slashing boosts block rewards; finality is determined by mempool fee rates.', False),
                ],
                'feedback': 'Slashing economically penalizes validator misbehavior, while finality is achieved when a supermajority of validators confirms checkpoints over epochs.'
            },
            {
                'text': 'Which of the following is NOT a course learning objective?',
                'choices': [
                    ('Master quantum computing basics', True),
                    ('Identify security challenges and solutions', False),
                    ('Develop and deploy smart contracts on Ethereum', False),
                    ('Understand blockchain principles and distributed ledgers', False),
                ],
                'feedback': 'The objectives include understanding blockchain principles, but not quantum computing basics.'
            },
            {
                'text': 'What is a key benefit of Merkle trees in blockchain?',
                'choices': [
                    ('Efficient membership proofs of size O(log n)', True),
                    ('Encrypting transaction data', False),
                    ('Storing full block data', False),
                    ('Performing consensus', False),
                ],
                'feedback': 'Merkle trees provide efficient membership proofs of size O(log n).'
            },
            {
                'text': 'SHA-1 is recommended for new blockchain designs.',
                'choices': [
                    ('True', False),
                    ('False', True),
                ],
                'feedback': 'No, SHA-1 is deprecated. SHA-256 and Keccak-256 are recommended.'
            },
            {
                'text': 'What does the FLP impossibility result state for fully asynchronous systems?',
                'choices': [
                    ('Synchronous clocks are required for consensus to be safe', False),
                    ('A majority of nodes must be Byzantine for consensus to fail', False),
                    ('Deterministic consensus cannot be guaranteed to terminate with even one faulty process', True),
                    ('Consensus is trivial with authenticated channels', False),
                ],
                'feedback': 'FLP shows that deterministic consensus may not terminate with even a single faulty process in a fully asynchronous model.'
            },
            {
                'text': 'Transaction fees on Ethereum are calculated as Gas Used * Gas Price. The Gas Price is commonly expressed in Gwei. What is the value of one Gwei in relation to ETH?',
                'choices': [
                    ('10^(-18) ETH', False),
                    ('10^9 ETH', False),
                    ('10^(-6) ETH', False),
                    ('10^(-9) ETH', True),
                ],
                'feedback': 'One Gwei is 1,000,000,000 Wei. Since 1 ETH = 10^18 Wei, one Gwei = 10^(-9) ETH.'
            },
            {
                'text': 'In the context of the Web3 stack, which component is uniquely responsible for cryptographically signing transactions on behalf of the user?',
                'choices': [
                    ('The user\'s Wallet (e.g., MetaMask)', True),
                    ('The frontend JavaScript library (e.g., Ethers.js)', False),
                    ('The JSON-RPC Node (e.g., Infura, Alchemy)', False),
                    ('The web browser', False),
                ],
                'feedback': 'The user\'s wallet is the only component that should have access to the user\'s private keys and is responsible for signing transactions.'
            },
            {
                'text': 'Which statement best defines a distributed system?',
                'choices': [
                    ('One powerful computer that time-slices tasks among users', False),
                    ('A collection of independent computers that work together and appear as a single coherent system', True),
                    ('Independent databases without any network communication', False),
                    ('Multiple processors sharing a single physical memory', False),
                ],
                'feedback': 'A distributed system is a collection of independent computers that appears as a single system to users.'
            },
            {
                'text': 'Which hash function is recommended for current blockchain designs?',
                'choices': [
                    ('SHA-256', True),
                    ('MD5', False),
                    ('SHA-1', False),
                    ('RIPEMD-160', False),
                ],
                'feedback': 'SHA-256 and Keccak-256 are currently recommended, while MD5 and SHA-1 are deprecated.'
            },
            {
                'text': 'Which validator action most commonly results in slashing penalties in Proof-of-Stake networks?',
                'choices': [
                    ('Running a validator on dedicated hardware.', False),
                    ('Paying lower transaction fees.', False),
                    ('Signing two conflicting blocks/attestations (double-signing).', True),
                    ('Remaining online with perfect uptime.', False),
                ],
                'feedback': 'Double-signing conflicting blocks or attestations is a classic slashing condition to deter equivocation.'
            },
            {
                'text': 'Which function visibility modifier allows a function to be called ONLY from outside the contract (not internally)?',
                'choices': [
                    ('private', False),
                    ('external', True),
                    ('public', False),
                    ('internal', False),
                ],
                'feedback': 'Functions marked as external can only be called from outside the contract. They cannot be called internally.'
            },
            {
                'text': 'What is the Bitcoin block subsidy (block reward excluding fees) after the most recent halving prior to 2025?',
                'choices': [
                    ('1.5625 BTC', False),
                    ('6.25 BTC', False),
                    ('12.5 BTC', False),
                    ('3.125 BTC', True),
                ],
                'feedback': 'After the 2024 halving, the block subsidy is 3.125 BTC per block.'
            },
            {
                'text': 'How does Proof of Work (PoW) provide Sybil resistance in permissionless networks?',
                'choices': [
                    ('By requiring costly computational work so that influence is proportional to hashpower, not identity count', True),
                    ('By limiting each IP address to a single node', False),
                    ('By encrypting all peer-to-peer traffic', False),
                    ('By using a central registry of approved miners', False),
                ],
                'feedback': 'PoW ties influence to computational work, making it costly to create many identities for undue influence.'
            },
            {
                'text': 'Which behavior best characterizes a Byzantine failure in distributed systems?',
                'choices': [
                    ('Permanent network disconnection', False),
                    ('Occasionally delayed but always truthful messages', False),
                    ('Arbitrary behavior, such as sending conflicting or malicious messages', True),
                    ('Only failing to respond to requests', False),
                ],
                'feedback': 'Byzantine nodes can behave arbitrarily, including sending conflicting or malicious messages.'
            },
            {
                'text': 'Name one required prerequisite for the course.',
                'choices': [
                    ('Basic Cryptography', True),
                    ('Computer Networks', False),
                    ('Programming', False),
                    ('Quantum Computing', False),
                ],
                'feedback': 'Required prerequisites include Basic Cryptography, Computer Networks, or Programming. Basic Cryptography is one correct answer.'
            },
            {
                'text': 'Many BFT-style PoS finality gadgets consider a block final when attestations meet which threshold?',
                'choices': [
                    ('More than 1/2 of validators.', False),
                    ('At least 3/4 of validators.', False),
                    ('At least 2/3 of validators.', True),
                    ('At least 1/3 of validators.', False),
                ],
                'feedback': 'BFT-style finality commonly requires supermajority agreement, typically at least 2/3 of validators.'
            },
            {
                'text': 'Which set lists fields typically found in a classic proof-of-work block header?',
                'choices': [
                    ('Merkle-Patricia state root, receipts root, logs bloom, difficulty, extradata', False),
                    ('Sender address, recipient address, gasLimit, gasPrice, signature', False),
                    ('Version, previous block hash, Merkle root, timestamp, target (nBits), nonce', True),
                    ('Account trie root, world-state hash, VM code size, base fee', False),
                ],
                'feedback': 'A classic header includes version, previous block hash, Merkle root, timestamp, target (nBits), and nonce.'
            },
            {
                'text': 'The project is worth 20% of the final grade.',
                'choices': [
                    ('True', True),
                    ('False', False),
                ],
                'feedback': 'Yes, project is 20%, midterm 30%, final 40%, quiz 10%.'
            },
            {
                'text': 'What is the primary purpose of events in Solidity smart contracts?',
                'choices': [
                    ('To log information for off-chain applications to monitor', True),
                    ('To reduce gas costs when modifying state variables', False),
                    ('To allow other smart contracts to read the contract\'s state', False),
                    ('To create backups of contract data', False),
                ],
                'feedback': 'Events provide a low-gas mechanism for contracts to log information that off-chain applications can listen to and react to.'
            },
            {
                'text': 'What is the main characteristic of a function marked with the view keyword in Solidity?',
                'choices': [
                    ('It can receive Ether', False),
                    ('It can read state but cannot modify it', True),
                    ('It can modify state variables', False),
                    ('It cannot read or modify state', False),
                ],
                'feedback': 'Functions marked as view can read the contract\'s state variables but cannot modify them. When called externally, they consume no gas.'
            },
            {
                'text': 'What happens due to the avalanche effect in hash functions?',
                'choices': [
                    ('A small change in input causes a drastic change in the digest', True),
                    ('The hash becomes slower to compute', False),
                    ('The hash function fails', False),
                    ('The output becomes longer', False),
                ],
                'feedback': 'A small change in input causes a drastic change in the digest - this is the avalanche effect.'
            },
            {
                'text': 'What is a critical issue with reusing nonces in ECDSA?',
                'choices': [
                    ('It reduces the signature size', False),
                    ('It leaks the secret key', True),
                    ('It improves hash security', False),
                    ('It speeds up verification', False),
                ],
                'feedback': 'Reusing nonces can leak the secret key.'
            },
            {
                'text': 'In Proof-of-Stake systems, a validator\'s chance of being selected to propose a block is primarily proportional to which quantity?',
                'choices': [
                    ('The transaction fees the validator has paid recently.', False),
                    ('The validator\'s IP address range.', False),
                    ('The amount of tokens the validator has staked.', True),
                    ('The validator\'s hash rate.', False),
                ],
                'feedback': 'Selection is typically proportional to stake and driven by cryptographic randomness (e.g., VRFs).'
            },
            {
                'text': 'Which book is NOT listed as a required textbook?',
                'choices': [
                    ('Mastering Ethereum by A.M. Antonopoulos & G. Wood', False),
                    ('Ethereum Yellow Paper', True),
                    ('Mastering Bitcoin by Andreas M. Antonopoulos', False),
                    ('Bitcoin and Cryptocurrency Technologies by Narayanan et al.', False),
                ],
                'feedback': 'The required books are Mastering Bitcoin, Mastering Ethereum, and Bitcoin and Cryptocurrency Technologies. The Yellow Paper is not listed as required.'
            },
            {
                'text': 'What is the primary reason an account-based blockchain uses Merkle-Patricia tries (MPT) for state?',
                'choices': [
                    ('To authenticate state with efficient inclusion proofs for accounts and storage keys.', True),
                    ('To implement proof-of-work difficulty adjustment.', False),
                    ('To compress transaction payloads.', False),
                    ('To schedule validator rotations deterministically each epoch.', False),
                ],
                'feedback': 'MPTs provide authenticated key-value state with efficient inclusion proofs and deterministic updates, enabling light-client verification.'
            },
            {
                'text': 'In Practical Byzantine Fault Tolerance (PBFT), how many matching replies does a client wait for before accepting a result? Assume up to f faulty replicas.',
                'choices': [
                    ('f + 1', True),
                    ('2f + 1', False),
                    ('n', False),
                    ('n - f', False),
                ],
                'feedback': 'The client waits for f + 1 matching replies to ensure at least one is from a correct replica.'
            },
            {
                'text': 'In Solidity, what is the relationship between uint and uint256?',
                'choices': [
                    ('uint is an alias for uint256', True),
                    ('uint can hold negative values while uint256 cannot', False),
                    ('uint is smaller and uses less gas than uint256', False),
                    ('uint is a dynamic type while uint256 is fixed', False),
                ],
                'feedback': 'uint is an alias for uint256. They are identical and represent a 256-bit unsigned integer.'
            },
            {
                'text': 'What effect describes a small change in input causing a huge change in hash output?',
                'choices': [
                    ('Avalanche effect', True),
                    ('Butterfly effect', False),
                    ('Cascade effect', False),
                    ('Ripple effect', False),
                ],
                'feedback': 'The avalanche effect describes how a small change in input causes a drastic change in the hash output.'
            },
            {
                'text': 'Why does the Ethereum Virtual Machine (EVM) not support floating-point arithmetic or true randomness?',
                'choices': [
                    ('To improve execution speed', False),
                    ('To save storage space', False),
                    ('To reduce gas costs', False),
                    ('To ensure deterministic execution across all nodes', True),
                ],
                'feedback': 'The EVM must be deterministic, meaning it produces identical results on every node for a given transaction.'
            },
            {
                'text': 'Attendance is mandatory for the course.',
                'choices': [
                    ('True', False),
                    ('False', True),
                ],
                'feedback': 'No, attendance is strongly recommended but not mandatory.'
            },
            {
                'text': 'A DApp needs to provide users with real-time notifications when a significant action occurs in a smart contract. What is the most efficient mechanism to achieve this?',
                'choices': [
                    ('Having the user manually refresh the page to see updates.', False),
                    ('Returning a value from the function that changes the state.', False),
                    ('Repeatedly calling a view function every few seconds to check for changes.', False),
                    ('Emitting an event from the smart contract and listening for it in the frontend.', True),
                ],
                'feedback': 'A smart contract can emit an event, which is a low-cost logging mechanism. Frontend applications can subscribe to these events to receive real-time updates.'
            },
            {
                'text': 'According to the CAP theorem, once a network partition occurs, a system must trade between which two properties?',
                'choices': [
                    ('Partition Tolerance and Availability', False),
                    ('Consistency and Availability', True),
                    ('Durability and Atomicity', False),
                    ('Latency and Throughput', False),
                ],
                'feedback': 'Under partition tolerance, a system must choose between strong consistency and availability.'
            },
            {
                'text': 'Which characteristic is most typical of a consortium (permissioned) blockchain compared to a public permissionless one?',
                'choices': [
                    ('Finality only after many confirmations with no strong guarantees.', False),
                    ('Known members identified via PKI with fast deterministic finality under BFT/CFT consensus.', True),
                    ('Pseudonymous identities and energy-based Sybil resistance.', False),
                    ('Anonymous membership with no onboarding controls.', False),
                ],
                'feedback': 'Permissioned systems use PKI-based identities, governance-defined onboarding, and often achieve fast deterministic finality using CFT/BFT consensus.'
            },
            {
                'text': 'Which is NOT a use of hashing in blockchain?',
                'choices': [
                    ('Block/Transaction IDs', False),
                    ('Encrypting private keys', True),
                    ('Proof-of-Work', False),
                    ('Address derivation', False),
                ],
                'feedback': 'Uses include block/tx IDs, PoW, address derivation, commitments; not directly for encryption.'
            },
            {
                'text': 'What do digital signatures NOT provide?',
                'choices': [
                    ('Confidentiality', True),
                    ('Authenticity', False),
                    ('Integrity', False),
                    ('Non-repudiation', False),
                ],
                'feedback': 'Digital signatures provide authenticity, integrity, and non-repudiation, but not confidentiality.'
            },
            {
                'text': 'What is the primary difference between require() and assert() in Solidity error handling?',
                'choices': [
                    ('require() consumes all gas while assert() refunds gas', False),
                    ('require() refunds remaining gas while assert() consumes all gas', True),
                    ('They are completely identical in behavior', False),
                    ('require() is for internal errors while assert() is for input validation', False),
                ],
                'feedback': 'require() is used for validating user inputs and refunds remaining gas on failure. assert() is used for internal errors and consumes all remaining gas on failure.'
            },
            {
                'text': 'Which sequence correctly describes the transaction flow in a Fabric-style permissioned ledger?',
                'choices': [
                    ('Commit state → order blocks → validate → simulate.', False),
                    ('Simulate and collect endorsements → order into blocks → validate (endorsement policy, MVCC) → commit state and ledger.', True),
                    ('Validate MVCC → endorse → order → commit.', False),
                    ('Order into blocks → simulate on all peers → commit → endorse.', False),
                ],
                'feedback': 'Fabric follows execute-order-validate: simulate and endorse to produce read/write sets; order into blocks; validate endorsement policy and MVCC; then commit.'
            },
            {
                'text': 'When you send a transaction using Ethers.js, you first receive a transaction response object. What is the primary purpose of then calling the await tx.wait() method on this object?',
                'choices': [
                    ('To get the transaction hash before the transaction is sent.', False),
                    ('To calculate and display the estimated gas fee to the user.', False),
                    ('To pause execution and wait until the transaction has been included in a block (i.e., confirmed).', True),
                    ('To ask the user to confirm the transaction in their wallet.', False),
                ],
                'feedback': 'tx.wait() pauses execution until the transaction is mined and included in a block, ensuring subsequent code runs against the confirmed state.'
            },
            {
                'text': 'In a Solidity smart contract, what does the global variable msg.sender represent?',
                'choices': [
                    ('The address of the immediate caller of the function', True),
                    ('The current block timestamp', False),
                    ('The address of the contract itself', False),
                    ('The amount of Ether sent with the transaction', False),
                ],
                'feedback': 'msg.sender is the address of the immediate caller of the current function. It is the most important variable for authentication and access control.'
            },
            {
                'text': 'After a client request is received, which ordering of the main PBFT agreement phases is correct?',
                'choices': [
                    ('Pre-prepare → Commit → Prepare', False),
                    ('Prepare → Commit → Pre-prepare', False),
                    ('Commit → Prepare → Reply', False),
                    ('Pre-prepare → Prepare → Commit', True),
                ],
                'feedback': 'The core phases proceed as Pre-prepare → Prepare → Commit, with quorums collected at Prepare and Commit.'
            },
            {
                'text': 'Which of the following is NOT a core property of smart contracts on blockchain platforms?',
                'choices': [
                    ('Deterministic', False),
                    ('Easily upgradeable', True),
                    ('Decentralized', False),
                    ('Immutable', False),
                ],
                'feedback': 'Smart contracts are immutable, deterministic, and decentralized, but they are not easily upgradeable once deployed.'
            },
            {
                'text': 'Which statement correctly distinguishes consensus rules from relay/mempool policy in a public blockchain network?',
                'choices': [
                    ('Policy is globally binding, while consensus rules are optional per node.', False),
                    ('Both are identical and must always match across nodes.', False),
                    ('Consensus rules are globally binding validity checks; policy is local relay/mining preference that can vary per node.', True),
                    ('Consensus rules only affect fees; policy determines block validity.', False),
                ],
                'feedback': 'Consensus rules determine block and transaction validity for all nodes; policy governs local relaying/mining preferences.'
            },
            {
                'text': 'In which week is the midterm exam scheduled?',
                'choices': [
                    ('Week 7', False),
                    ('Week 8', False),
                    ('Week 9', True),
                    ('Week 10', False),
                ],
                'feedback': 'The midterm exam is scheduled in Week 9.'
            },
            {
                'text': 'Which software is NOT listed in the course resources?',
                'choices': [
                    ('VS Code with blockchain extensions', False),
                    ('MetaMask wallet', False),
                    ('Adobe Photoshop', True),
                    ('Git & GitHub', False),
                ],
                'feedback': 'Listed resources include Solidity environment, MetaMask, Git, VS Code. Adobe Photoshop is not listed.'
            },
            {
                'text': 'What is the scheduled time for the COMP4211 class?',
                'choices': [
                    ('Monday 20:00-22:45', True),
                    ('Tuesday 18:00-20:45', False),
                    ('Friday 20:00-22:45', False),
                    ('Wednesday 19:00-21:45', False),
                ],
                'feedback': 'The class is scheduled for Monday 20:00-22:45.'
            },
            {
                'text': 'For an n-bit hash, collisions are expected after approximately how many trials?',
                'choices': [
                    ('2^n trials', False),
                    ('2^(n/2) trials', True),
                    ('n trials', False),
                    ('n^2 trials', False),
                ],
                'feedback': 'Due to the birthday paradox, collisions are expected after approximately 2^(n/2) trials.'
            },
            {
                'text': 'Which property of hash functions makes it hard to find two different inputs with the same output? (Duplicate check)',
                'choices': [
                    ('Second preimage resistance', False),
                    ('Collision resistance', True),
                    ('Avalanche effect', False),
                    ('Preimage resistance', False),
                ],
                'feedback': 'Collision resistance ensures it is hard to find any x ≠ x\' with h(x) = h(x\').'
            },
            {
                'text': 'Which curve is the Bitcoin standard for ECDSA? (Repeat)',
                'choices': [
                    ('Ed25519', False),
                    ('Curve25519', False),
                    ('secp256r1', False),
                    ('secp256k1', True),
                ],
                'feedback': 'secp256k1 is the Bitcoin standard for ECDSA.'
            },
            {
                'text': 'What is a key benefit of Merkle trees in blockchain? (Verification)',
                'choices': [
                    ('Perform consensus', False),
                    ('Provide membership proofs of size O(log n)', True),
                    ('Encrypt transactions', False),
                    ('Store full block data', False),
                ],
                'feedback': 'Efficient membership proofs of size O(log n).'
            },
            {
                'text': 'What effect describes a small change in input causing a huge change in hash output? (Review)',
                'choices': [
                    ('Avalanche effect', True),
                    ('Butterfly effect', False),
                    ('Cascade effect', False),
                    ('Ripple effect', False),
                ],
                'feedback': 'Avalanche effect.'
            },
        ]

        self._load_questions(session, questions)

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] All COMP4211 Midterm questions loaded successfully!'))
        self.stdout.write(f'Total questions in Midterm: {session.questions.count()}')

    def _load_questions(self, session, questions_data):
        """Helper method to load questions into a session"""
        existing_count = session.questions.count()
        created_count = 0
        updated_count = 0
        
        for idx, q_data in enumerate(questions_data, start=1):
            # Check if question with same text already exists
            question = Question.objects.filter(
                session=session,
                text=q_data['text']
            ).first()
            
            if question:
                # Question exists, update order and ensure it's active
                question.order = idx
                question.is_active = True
                question.save(update_fields=['order', 'is_active'])
                
                # Update choices if they exist, otherwise create them
                existing_choices = list(question.choices.all())
                if len(existing_choices) == len(q_data['choices']):
                    # Update existing choices
                    for choice, (choice_text, is_correct) in zip(existing_choices, q_data['choices']):
                        choice.text = choice_text
                        choice.is_correct = is_correct
                        choice.save(update_fields=['text', 'is_correct'])
                else:
                    # Delete old choices and create new ones
                    question.choices.all().delete()
                    for choice_text, is_correct in q_data['choices']:
                        Choice.objects.create(
                            question=question,
                            text=choice_text,
                            is_correct=is_correct
                        )
                
                updated_count += 1
                self.stdout.write(f'  [~] Updated question {idx}')
            else:
                # Create new question
                question = Question.objects.create(
                    session=session,
                    text=q_data['text'],
                    order=idx,
                    is_active=True
                )
                
                # Create choices for this question
                for choice_text, is_correct in q_data['choices']:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
                created_count += 1
                self.stdout.write(f'  [+] Created question {idx}')
        
        self.stdout.write(f'\nSummary: Created {created_count} questions, updated {updated_count} questions.')

