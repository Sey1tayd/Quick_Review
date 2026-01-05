from django.core.management.base import BaseCommand
from django.db.models import Max
from quiz.models import Course, Session, Question, Choice
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Adds questions for COMP4211'

    def handle(self, *args, **options):
        # Create or get course
        course, created = Course.objects.get_or_create(
            slug='comp4211',
            defaults={'title': 'COMP4211'}
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
                'text': "What is the primary requirement of the 'Travel Rule' as applied to Virtual Asset Service Providers (VASPs)?",
                'choices': [
                    ('Originator and beneficiary information must accompany transfers between service providers.', True),
                    ('Users must physically travel to a registered kiosk to perform large transactions.', False),
                    ("All private keys must be stored in a geographic location matching the user's citizenship.", False),
                    ('Blockchain transactions must be delayed byTdelayto allow for manual inspection.', False),
                ]
            },
            {
                'text': 'Which option isnotone of the three classic functions of money?',
                'choices': [
                    ('Store of value', False),
                    ('Medium of exchange', False),
                    ('Unit of account', False),
                    ('Consensus mechanism', True),
                ]
            },
            {
                'text': "Which stablecoin design is generally most exposed to a 'death spiral' dynamic during stress, where loss of confidence triggers reflexive selling and further depegging?",
                'choices': [
                    ('Fiat-collateralized stablecoins backed 1:1 by cash or short-term treasuries', False),
                    ('Crypto-collateralized stablecoins that are over-collateralized on-chain', False),
                    ('Algorithmic stablecoins without hard collateral backing', True),
                    ('Central bank digital currencies issued by a central bank', False),
                ]
            },
            {
                'text': 'A key claim of Bitcoin-like systems is that they enable verifiable digital scarcity (e.g., a cap such as21×106units) without relying on a trusted third party. What best explains this?',
                'choices': [
                    ('A public ledger with consensus rules that anyone can verify', True),
                    ('A central administrator who approves each transaction', False),
                    ('Private databases mirrored by multiple banks', False),
                    ('Keeping balances secret so no one can audit supply', False),
                ]
            },
            {
                'text': 'Which statement best describes the UTXO (Unspent Transaction Output) model commonly associated with early cryptocurrencies?',
                'choices': [
                    ('Coins are represented as discrete outputs that can be spent as inputs in new transactions', True),
                    ('Each user has exactly one global balance variable updated in place', False),
                    ('Transactions are valid only if a bank signs them', False),
                    ('Tokens can only be created by upgrading the protocol', False),
                ]
            },
            {
                'text': 'In a typical ERC-20 spending workflow, which pair of actions enables a third party (a spender) to transfer tokens from an owner’s address within a defined limit?',
                'choices': [
                    ('Owner callsapprove, then spender callstransferFrom', True),
                    ('Spender callsbalanceOf, then callstotalSupply', False),
                    ('Owner callstransfer, then callsbalanceOf', False),
                    ('Spender callstransfer, then owner callsallowance', False),
                ]
            },
            {
                'text': 'Which token standard is most closely associated with representinguniqueassets where each token ID can be distinct?',
                'choices': [
                    ('ERC-20', False),
                    ('ERC-721', True),
                    ('ERC-4626', False),
                    ('ERC-2612', False),
                ]
            },
            {
                'text': 'Which option isnottypically considered one of the core DeFi primitives?',
                'choices': [
                    ('Lending / borrowing', False),
                    ('Decentralized exchanges', False),
                    ('Derivatives', False),
                    ('Mandatory identity verification (KYC) layers', True),
                ]
            },
            {
                'text': 'In an over-collateralized lending system, a borrower may be required to maintain a collateral ratio such as150%. What does this imply?',
                'choices': [
                    ('Collateral value must be at least1.5×the loan value', True),
                    ('The borrower can borrow without posting any collateral', False),
                    ('The lender guarantees the peg of a stablecoin', False),
                    ('The loan is automatically interest-free', False),
                ]
            },
            {
                'text': 'Which statement best defines a flash loan in decentralized finance?',
                'choices': [
                    ('A loan that must be borrowed and repaid within the same blockchain transaction', True),
                    ('A long-term loan with fixed monthly payments', False),
                    ('A loan that requires KYC before borrowing', False),
                    ('A loan backed by government deposit insurance', False),
                ]
            },
            {
                'text': 'Automated market makers with concentrated liquidity allow liquidity providers (LPs) to choose a price range (e.g.,1500–2500for an ETH-stablecoin pair). What is the main intended benefit?',
                'choices': [
                    ('Higher capital efficiency by allocating liquidity only within selected price ranges', True),
                    ('Guaranteeing a fixed exchange rate at all times', False),
                    ('Eliminating all trading fees for users', False),
                    ('Preventing arbitrage across markets', False),
                ]
            },
            {
                'text': 'What is the primary design principle when applying blockchain to Electronic Health Records (EHR)?',
                'choices': [
                    ('Using blockchain as a coordination and audit layer for access events and record hashes.', True),
                    ('Storing all sensitive medical files and lab results directly on the public ledger.', False),
                    ('Replacing hospital databases with a single, globally shared Ethereum contract.', False),
                    ('Granting full, transparent access to all patient data to every node in the network.', False),
                ]
            },
            {
                'text': 'In a Proof-of-Work blockchain, what is the primary resource required for an attacker to successfully execute a 51% attack to revert confirmed transactions?',
                'choices': [
                    ("More than 50% of the network's total hashing power", True),
                    ('A majority of the unique IP addresses in the P2P network', False),
                    ('Control over the Border Gateway Protocol (BGP) routing', False),
                    ('Ownership of 51% of the total circulating token supply', False),
                ]
            },
            {
                'text': 'Why is it often possible to de-anonymize users on public blockchains like Bitcoin or Ethereum despite the use of pseudonymous addresses?',
                'choices': [
                    ('Transaction graph analysis and address clustering heuristics can link activity to real-world identities.', True),
                    ('The blockchain protocol requires users to attach their name to every block.', False),
                    ('Private keys are automatically shared with the network nodes for verification.', False),
                    ('Mining pools are required by law to publish the identities of all transactors.', False),
                ]
            },
            {
                'text': 'When comparing Central Bank Digital Currencies (CBDCs) and private stablecoins, which dimension is typically a strength of private stablecoins but a limitation for CBDCs?',
                'choices': [
                    ('Full monetary policy control', False),
                    ('Speed of innovation and global accessibility', True),
                    ('Government backing and legal tender status', False),
                    ('Offline capability in domestic retail', False),
                ]
            },
            {
                'text': 'How does blockchain technology mitigate the risk of selective reporting or data tampering in clinical trials?',
                'choices': [
                    ('By timestamping key milestones and data commitments on an immutable ledger.', True),
                    ('By automatically recruiting patients through decentralized social media.', False),
                    ('By ensuring all trial outcomes are kept secret from regulators.', False),
                    ('By removing the need for patient consent through smart contract logic.', False),
                ]
            },
            {
                'text': 'When mapping a blockchain product to regulatory regimes, which four dimensions must be considered to avoid compliance failures?',
                'choices': [
                    ('Asset, Actor, Activity, and Jurisdiction.', True),
                    ('Protocol, Consensus, Hashrate, and Distribution.', False),
                    ('Validation, Mining, Staking, and Minting.', False),
                    ('Encryption, Scalability, Liquidity, and Interoperability.', False),
                ]
            },
            {
                'text': "In a 'Compliance-by-Design' framework, which layer is responsible for implementable controls such as key management, access control, and logging?",
                'choices': [
                    ('The Technical Layer.', True),
                    ('The Policy Layer.', False),
                    ('The Process Layer.', False),
                    ('The Assurance Layer.', False),
                ]
            },
            {
                'text': 'When scoping compliance for a blockchain product, which set of dimensions is the most useful starting map to reduce missed obligations?',
                'choices': [
                    ('Asset, actor, activity, jurisdiction', True),
                    ('Consensus, block size, node count, hash rate', False),
                    ('UI layout, brand color, marketing slogan, app store rating', False),
                    ('CPU model, memory size, disk type, network driver', False),
                ]
            },
            {
                'text': 'In many blockchain services, a central consumer-protection question is: who bears responsibility when funds are lost. Which design fact most directly determines this?',
                'choices': [
                    ('Who controls the private keys (self-custody vs third-party custody)', True),
                    ('Whether blocks are mined or validated', False),
                    ('Whether the UI uses dark mode', False),
                    ('Whether transaction fees are paid in token A or token B', False),
                ]
            },
            {
                'text': 'According to the standard economic definitions used to evaluate cryptocurrencies like Bitcoin, which of the following represents the three primary roles of money?',
                'choices': [
                    ('Store of Value, Medium of Exchange, and Unit of Account', True),
                    ('Fungibility, High Friction, and Centralized Issuance', False),
                    ('Programmability, Speculation, and Government Backing', False),
                    ('Privacy, Liquidity, and Infinite Supply', False),
                ]
            },
            {
                'text': 'In the context of the real economy beyond digital money, what is the primary question to consider when evaluating whether to implement a blockchain solution?',
                'choices': [
                    ('Where does decentralization provide a net benefit over centralized platforms?', True),
                    ('How can we replace all traditional databases with smart contracts?', False),
                    ('What is the maximum transaction speed of the underlying network?', False),
                    ('How can we eliminate the need for any off-chain storage?', False),
                ]
            },
            {
                'text': 'What is the role of a DID Document in a decentralized identity system?',
                'choices': [
                    ('It contains public keys, authentication methods, and service endpoints associated with the DID.', True),
                    ("It stores the user's full name, address, and physical biometric data on the blockchain.", False),
                    ('It serves as a central registry that verifies every login attempt in real-time.', False),
                    ('It is a physical document that must be scanned to access the blockchain.', False),
                ]
            },
            {
                'text': "A project claims 'no one is responsible because it is decentralized'. Which factor most strongly suggests regulators may still identify responsible parties?",
                'choices': [
                    ('A small group controls admin keys and can upgrade contracts or set key parameters', True),
                    ('The protocol uses peer-to-peer gossip', False),
                    ('Transactions are visible on a block explorer', False),
                    ('Users can run nodes if they want to', False),
                ]
            },
            {
                'text': "In the context of 'Money Legos' or DeFi primitives, which decentralized component serves as the equivalent to traditional stock exchanges like NASDAQ or the NYSE?",
                'choices': [
                    ('Decentralized Exchanges (DEXs)', True),
                    ('Liquid Staking Protocols', False),
                    ('Lending and Borrowing Markets', False),
                    ('Central Bank Digital Currencies (CBDCs)', False),
                ]
            },
            {
                'text': 'What is the primary security risk when a smart contract uses thedelegatecallopcode to interact with an external, untrusted contract?',
                'choices': [
                    ("The external contract can modify the calling contract's internal state and storage directly.", True),
                    ('The external contract can only read the state but cannot send Ether.', False),
                    ('It increases the gas cost of the transaction beyond the block limit.', False),
                    ('It forces the transaction to be public even if using a privacy mixer.', False),
                ]
            },
            {
                'text': 'Which type of attack involves an adversary monopolizing all incoming and outgoing connections of a specific victim node to isolate it from the rest of the honest network?',
                'choices': [
                    ('Eclipse Attack', True),
                    ('Sybil Attack', False),
                    ('Finney Attack', False),
                    ('Reentrancy Attack', False),
                ]
            },
            {
                'text': "Since core decentralized protocols are difficult to regulate directly, where does regulatory enforcement typically 'attach' in the ecosystem?",
                'choices': [
                    ('Practical control points like Web UIs, fiat on/off-ramps, and hosted wallet providers.', True),
                    ('The underlying mathematical hash functions used for block validation.', False),
                    ('The distributed peer-to-peer gossip network itself.', False),
                    ('Individual miners who contribute less than1%of the total network hashrate.', False),
                ]
            },
            {
                'text': 'In practice, where do authorities most often attach enforcement and compliance obligations in blockchain ecosystems?',
                'choices': [
                    ('Operators of accountable interfaces and rails (front-ends, custody, exchanges, fiat on/off-ramps)', True),
                    ('Random users who merely read the ledger', False),
                    ('Only miners/validators, regardless of their role', False),
                    ('Only the authors of academic papers about the protocol', False),
                ]
            },
            {
                'text': 'TheIERC20interface defines a standard for fungible tokens. Which of the following functions is used to give a third party the permission to spend a specific amount of tokens on behalf of the owner?',
                'choices': [
                    ('transfer(addressto,uint256amount)', False),
                    ('approve(addressspender,uint256amount)', True),
                    ('balanceOf(addressaccount)', False),
                    ('totalSupply()', False),
                ]
            },
            {
                'text': 'Beyond legal compliance, which of the following is considered a common ethical risk that should be mitigated in blockchain projects?',
                'choices': [
                    ('Predatory tokenomics and exclusion of users via high fees or complex UX.', True),
                    ('UtilizingSHA-256instead ofEthashfor consensus.', False),
                    ('Implementing a timelock for protocol upgrades.', False),
                    ('Publishing independent audit reports to the public.', False),
                ]
            },
            {
                'text': "In the evolution of blockchain-based assets, which milestone primarily enabled the transition from simple native coins to 'programmable money' and the subsequent explosion of DeFi?",
                'choices': [
                    ('The launch of Bitcoin as a native UTXO coin in 2009', False),
                    ('The introduction of Ether and smart contracts in 2015', True),
                    ('The creation of Colored Coins on the Bitcoin network in 2012', False),
                    ('The development of the ERC-721 standard for non-fungible tokens in 2018', False),
                ]
            },
            {
                'text': 'Which set best represents core AML/CFT controls commonly expected from regulated financial service providers?',
                'choices': [
                    ('Customer due diligence, suspicious activity monitoring, reporting, and recordkeeping', True),
                    ('Removing all logs to maximize privacy', False),
                    ('Guaranteeing irreversible anonymity for every user', False),
                    ('Increasing leverage limits to attract more trading volume', False),
                ]
            },
            {
                'text': "What is the defining characteristic of a 'flash loan' in decentralized finance?",
                'choices': [
                    ('It requires over-collateralization with high-volatility crypto assets', False),
                    ('It requires no collateral, provided the funds are borrowed and repaid within the same transaction', True),
                    ('It is a long-term loan used exclusively for real-world retail payments', False),
                    ('It is a private loan issued only by Central Banks to commercial banks', False),
                ]
            },
            {
                'text': "Predictions for the year 2030 often suggest a 'hybrid world' for the money layer. In this scenario, what is the most likely distribution of digital money usage?",
                'choices': [
                    ('Regulated private stablecoins for international payments/DeFi and CBDCs for domestic retail', True),
                    ('Bitcoin replacing all central banks and government currencies globally', False),
                    ('The total disappearance of private stablecoins in favor of physical cash', False),
                    ('CBDCs becoming the only form of money used for both domestic and international trade', False),
                ]
            },
            {
                'text': "Which governance model is characterized by broad participation and token-based voting, but often faces challenges with ambiguous liability and 'capture risk'?",
                'choices': [
                    ('DAO Governance.', True),
                    ('Centralized Operator.', False),
                    ('Foundation with Multi-sig.', False),
                    ('Single-entity Platform.', False),
                ]
            },
            {
                'text': 'Which of the following is a major challenge in decentralized identity regarding the loss of private keys?',
                'choices': [
                    ('The need for social recovery or secure key management strategies to prevent loss of access.', True),
                    ('The requirement that all private keys must be stored in a centralized government vault.', False),
                    ('The inability of the blockchain to process more thanα=10identities per second.', False),
                    ('The law that mandates all digital identities must be reset every year.', False),
                ]
            },
            {
                'text': "Modern Solidity development (version 0.8 and above) has significantly reduced the risk of 'BeautyChain' style exploits because:",
                'choices': [
                    ('Arithmetic overflow and underflow checks are built-in by default.', True),
                    ('The EVM now supports infinite precision integers.', False),
                    ('All transactions are now processed off-chain in ZK-Rollups.', False),
                    ('Public functions are no longer allowed to acceptuintparameters.', False),
                ]
            },
            {
                'text': 'Which feature most strongly increases the chance that a token will be treated under securities-style rules?',
                'choices': [
                    ('Marketing that emphasizes profit expectation from a team’s ongoing efforts', True),
                    ('Using a Merkle tree for state commitments', False),
                    ('Having a fixed maximum supply', False),
                    ('Using peer-to-peer networking instead of client-server', False),
                ]
            },
            {
                'text': 'Why has liquid staking, such as using ETH to receivestETH, become a significant part of the blockchain ecosystem?',
                'choices': [
                    ('It allows users to earn staking rewards without losing the liquidity of their assets', True),
                    ('It guarantees that the price of the token will remain fixed to the US Dollar', False),
                    ('It removes the need for any underlying blockchain security', False),
                    ('It converts fungible tokens into unique non-fungible tokens (NFTs)', False),
                ]
            },
            {
                'text': 'In a blockchain-enabled supply chain, which of the following is most appropriate to storeon-chain?',
                'choices': [
                    ('Asset identifiers and cryptographic hashes of documents.', True),
                    ('High-resolution images and videos of product assembly.', False),
                    ('Proprietary internal ERP data and employee payroll.', False),
                    ('Large PDF files containing multi-year compliance certifications.', False),
                ]
            },
            {
                'text': "Which design 'rule of thumb' is recommended to balance transparency with privacy and data protection compliance?",
                'choices': [
                    ('Keep personal data off-chain and only store proofs or commitments on-chain.', True),
                    ('Encrypt all personal data and store it permanently on a public ledger.', False),
                    ('Anonymize all data using mixers before recording it on a permissionless chain.', False),
                    ('Only use permissionless ledgers for financial transactions involving identity.', False),
                ]
            },
            {
                'text': 'Which privacy-focused cryptocurrency is known for utilizing a combination of Ring Signatures, Stealth Addresses, and RingCT to hide the sender, receiver, and transaction amount?',
                'choices': [
                    ('Monero', True),
                    ('Bitcoin Gold', False),
                    ('Ethereum Classic', False),
                    ('Zcash', False),
                ]
            },
            {
                'text': 'Which architecture best supports compliance-friendly privacy on a transparent ledger while reducing personal data exposure?',
                'choices': [
                    ('Store personal data off-chain and store only commitments/proofs on-chain (e.g.,c=H(data))', True),
                    ('Put full names, addresses, and medical records directly on a public ledger', False),
                    ('Disable all auditing and monitoring to protect privacy', False),
                    ('Use larger blocks so that personal data is harder to find', False),
                ]
            },
            {
                'text': 'In the context of blockchain system design, which of the following represents a primary tension between core technology features and regulatory requirements?',
                'choices': [
                    ('The conflict between immutability and the legal right to correct or delete personal data.', True),
                    ('The conflict between high throughput and energy efficiency standards.', False),
                    ('The conflict between proof-of-work mechanisms and anti-money laundering reporting.', False),
                    ('The conflict between smart contract execution speed and tax reporting deadlines.', False),
                ]
            },
            {
                'text': 'A blockchain application stores user personal data directly on-chain. Which legal/regulatory tension is most directly triggered by this design choice?',
                'choices': [
                    ('Immutability vs the right-to-correct/delete data', True),
                    ('Decentralization vs low transaction fees', False),
                    ('Encryption vs hash function selection', False),
                    ('Latency vs throughput in consensus', False),
                ]
            },
            {
                'text': 'When determining liability in a supposedly decentralized system, what do regulators and courts primarily look for?',
                'choices': [
                    ('Actual control and benefit, such as who manages admin keys, front-ends, or fee collection.', True),
                    ('The total number of nodes currently running the software protocol.', False),
                    ('Whether the source code is licensed under an open-source agreement.', False),
                    ('The mathematical complexity of the consensus algorithmCalgo.', False),
                ]
            },
            {
                'text': 'Which of the following best describes the core concept of Self-Sovereign Identity (SSI)?',
                'choices': [
                    ('The user controls their own identifiers and credentials in a digital wallet without a central provider.', True),
                    ('Users log in to all services using a single account provided by a major tech company.', False),
                    ('A national government manages all digital identities in a centralized database.', False),
                    ('Each service provider creates a separate, siloed account for every individual user.', False),
                ]
            },
            {
                'text': 'According to the strategy proposed by Eyal and Sirer, a selfish miner can potentially earn disproportionate revenue by withholding blocks and releasing them strategically, even if they only control approximately what percentage of the total hash power?',
                'choices': [
                    ('33%', True),
                    ('10%', False),
                    ('51%', False),
                    ('75%', False),
                ]
            },
            {
                'text': 'How can smart contracts automate business rules within a logistics network?',
                'choices': [
                    ('By triggering automatic payments or penalties based on IoT sensor events.', True),
                    ('By physically moving goods between warehouses using blockchain protocols.', False),
                    ('By replacing the need for legal regulators and customs authorities.', False),
                    ('By eliminating the requirement for any digital identifiers on physical goods.', False),
                ]
            },
            {
                'text': "To prevent reentrancy and other logic-based exploits, developers are encouraged to follow the 'Checks-Effects-Interactions' pattern. This means:",
                'choices': [
                    ('Internal state updates (e.g., balance reductions) should happen before any external contract calls or Ether transfers.', True),
                    ('External calls should be made first to ensure the recipient is valid before updating local state.', False),
                    ("Contracts should always use theblockhashto verify the caller's identity.", False),
                    ("All functions should be set to 'public' by default to ensure transparency.", False),
                ]
            },
            {
                'text': 'In the context of the famous DAO hack, how does a reentrancy vulnerability allow an attacker to drain funds?',
                'choices': [
                    ("By calling the withdraw function repeatedly before the contract updates the attacker's balance.", True),
                    ('By overflowing auint256variable to make a small balance appear massive.', False),
                    ("By using delegatecall to execute malicious code in the context of the target's storage.", False),
                    ("By manipulating the block's timestamp to predict random outcomes.", False),
                ]
            },
            {
                'text': 'As of late 2025, which regulatory approach has been adopted by the European Union through the MiCA framework regarding stablecoins?',
                'choices': [
                    ('A total ban on all digital assets and blockchain technology', False),
                    ('A complete lack of federal framework, relying on state-level licenses', False),
                    ('A fully live licensing system where tokens like USDC must meet specific reserve requirements', True),
                    ('Mandatory use of the e-CNY for all private transactions', False),
                ]
            },
            {
                'text': "Which type of stablecoin is associated with 'death spiral' risks, where a loss of confidence leads to hyperinflation of a secondary seigniorage token and a total collapse, as seen with Terra/Luna?",
                'choices': [
                    ('Fiat-collateralized stablecoins', False),
                    ('Crypto-collateralized stablecoins', False),
                    ('Algorithmic stablecoins', True),
                    ('Central Bank Digital Currencies (CBDCs)', False),
                ]
            },
            {
                'text': 'Which concern is most specific to stablecoins compared to many non-pegged tokens?',
                'choices': [
                    ('Reserve quality, redemption rights, and run-risk management', True),
                    ('Whether the token uses elliptic curves', False),
                    ('Whether transactions are batched into blocks', False),
                    ('Whether nodes run on Linux', False),
                ]
            },
            {
                'text': 'What is considered a major pain point in traditional supply chains that a permissioned blockchain aims to solve?',
                'choices': [
                    ('Data being siloed across many inconsistent IT systems that are hard to audit.', True),
                    ('The excessive use of IoT sensors and GPS tracking by logistics providers.', False),
                    ('The lack of physical manufacturers in the production cycle.', False),
                    ('The inability to generate invoices or electronic payments.', False),
                ]
            },
            {
                'text': 'Under which condition is a token most likely to be regulated under securities-style rules?',
                'choices': [
                    ('If the token functions like an investment with an expectation of profit based on the efforts of others.', True),
                    ('If the token is used solely for voting on technical protocol upgrades.', False),
                    ('If the token is only used to pay for transaction fees on a decentralized network.', False),
                    ('If the token is restricted to a private, permissioned ledger with no secondary market.', False),
                ]
            },
            {
                'text': 'A token originally marketed as providing platform access later becomes widely promoted with profit expectations and strong issuer control. What is the best statement about token classification risk?',
                'choices': [
                    ('Token classification can shift as marketing, rights, and control structures evolve', True),
                    ('Classification is fixed at minting and cannot change afterward', False),
                    ('Only the token ticker symbol determines classification', False),
                    ('Classification depends only on block time, not economics or governance', False),
                ]
            },
            {
                'text': "In the context of transfers between virtual asset service providers, what does the 'Travel Rule' concept generally require?",
                'choices': [
                    ('Originator and beneficiary information may need to accompany the transfer', True),
                    ('Every transaction must be reversed within 24 hours', False),
                    ('All smart contracts must be open-sourced', False),
                    ('Validators must disclose their hardware serial numbers', False),
                ]
            },
            {
                'text': 'In the Verifiable Credentials trust triangle, what is the role of theHolder?',
                'choices': [
                    ('To receive signed credentials from an issuer and present proofs to a verifier.', True),
                    ('To cryptographically sign the original credential and verify its authenticity.', False),
                    ('To manage the blockchain network and approve all transactions.', False),
                    ('To store all personally identifiable information on the public ledger.', False),
                ]
            },
            {
                'text': 'In multi-organization workflows (e.g., logistics, healthcare networks), which situation most strongly suggests a blockchain-based shared ledger could add value compared to a single centralized database?',
                'choices': [
                    ('Multiple independent organizations need a shared, tamper-evident event history, and no single party is trusted to operate the system alone.', True),
                    ('A single company controls all data and all users fully trust that company to manage access and logs.', False),
                    ('The primary requirement is storing large media files (e.g., videos, MRI images) directly inside the database layer.', False),
                    ('The main goal is achieving the lowest possible latency for a single application’s internal transactions.', False),
                ]
            },
            {
                'text': 'In self-sovereign identity systems, why is reusing the same identifier across many services considered a privacy risk?',
                'choices': [
                    ('It enables cross-service correlation and tracking by linking a user’s actions across contexts to one identifier.', True),
                    ('It prevents any verifier from checking signatures, because identifiers must be unique per day.', False),
                    ('It makes credentials impossible to revoke, since revocation requires a new blockchain.', False),
                    ('It forces users to publish all personal attributes on-chain to keep the identifier valid.', False),
                ]
            },
            {
                'text': 'In real-world blockchain systems that manage documents (certificates, reports, IoT logs), what is a common reason to store a document hash on-chain while keeping the full document off-chain?',
                'choices': [
                    ('To make off-chain data tamper-evident while avoiding storing large or sensitive files directly on the blockchain.', True),
                    ('To encrypt the document automatically, since any on-chain hash is inherently secret.', False),
                    ('To ensure the document can be deleted from all copies instantly when requested.', False),
                    ('To guarantee that only one organization can access the document without any access control logic.', False),
                ]
            },
            {
                'text': 'Which example best illustrates how a smart contract can automate a business rule in a supply network?',
                'choices': [
                    ('Releasing payment automatically after delivery is confirmed by a signed handover event.', True),
                    ('Storing all sensor readings and video footage on-chain to reduce storage costs.', False),
                    ('Replacing cryptographic signatures with manual email approvals to simplify auditing.', False),
                    ("Guaranteeing that external data sources can never be incorrect because they are called 'oracles'.", False),
                ]
            },
            {
                'text': 'In an anti-counterfeit product system, which mechanism most directly helps detect a forged item that attempts to mimic a legitimate identifier?',
                'choices': [
                    ('Logging custody transfers so verifiers can check whether the identifier’s history is consistent and not duplicated.', True),
                    ('Allowing anyone to overwrite past ledger entries if they provide a convincing explanation.', False),
                    ('Using a single shared password among all supply chain parties to speed up access.', False),
                    ('Publishing all proprietary manufacturing recipes on-chain to prove authenticity.', False),
                ]
            },
            {
                'text': 'Which statement best reflects a practical limitation of using blockchains in healthcare data systems?',
                'choices': [
                    ('Blockchains are generally not suitable for storing large medical files directly, and privacy needs can conflict with full transparency.', True),
                    ('Blockchains automatically guarantee interoperability between all hospital systems without any integration work.', False),
                    ('Medical records become public by default if a permissioned network is used.', False),
                    ('Audit logs are impossible to implement using cryptographic signatures and timestamps.', False),
                ]
            },
            {
                'text': 'In a patient-centric architecture that uses blockchain as an audit layer, which information is most appropriate to record on-chain?',
                'choices': [
                    ('Signed access events and hashes of record versions to support integrity checks and auditability.', True),
                    ('Full clinical notes and all imaging files, stored as raw binary blobs to maximize transparency.', False),
                    ('Patients’ complete personal profiles (PII) in plain text so every participant can search them quickly.', False),
                    ('Temporary cache copies of hospital databases for faster analytics.', False),
                ]
            },
            {
                'text': 'A consent smart contract in a healthcare-sharing system most naturally encodes which type of rule?',
                'choices': [
                    ('Allowing specific providers to access specific data types for a defined purpose and time window.', True),
                    ('Guaranteeing that any provider can access all patient data forever once they are in the network.', False),
                    ("Replacing authentication keys with a shared 'network master password' for simplicity.", False),
                    ('Deleting all historical access logs whenever a patient updates a consent preference.', False),
                ]
            },
            {
                'text': 'Which description best matches a Decentralized Identifier (DID)?',
                'choices': [
                    ('A globally unique identifier that can be resolved without a centralized registry, typically linked to a document containing public keys and endpoints.', True),
                    ('A username that must be issued and approved by a single global authority before it can be used.', False),
                    ('A password format that replaces public-key cryptography with shared secrets.', False),
                    ('A payment address that is valid only for cryptocurrencies and cannot represent organizations or services.', False),
                ]
            },
            {
                'text': 'In the issuer–holder–verifier model for verifiable credentials, which role is responsible for creating and cryptographically signing the credential?',
                'choices': [
                    ('Issuer', True),
                    ('Holder', False),
                    ('Verifier', False),
                    ('Oracle', False),
                ]
            },
            {
                'text': 'In a proof-of-work blockchain, an adversary temporarily controlling more than half of the total hashing power can most directly enable which outcome?',
                'choices': [
                    ('Reorganizing recent blocks to reverse confirmed transactions and perform double-spending', True),
                    ('Permanently forging signatures for any address without private keys', False),
                    ('Reading encrypted wallet seed phrases from the network', False),
                    ('Guaranteeing faster transaction finality for all users', False),
                ]
            },
            {
                'text': 'Which description best matches the core strategy behind selfish mining?',
                'choices': [
                    ('Withholding blocks to maintain a private chain and releasing it at strategic times to cause honest blocks to become stale', True),
                    ('Broadcasting every found block immediately to maximize decentralization', False),
                    ('Generating many fake identities to outvote peers in the P2P layer', False),
                    ('Encrypting all transactions so that miners cannot see transaction contents', False),
                ]
            },
            {
                'text': 'In an eclipse attack against a blockchain node, the attacker primarily attempts to:',
                'choices': [
                    ("Monopolize the victim's network connections to isolate it from honest peers", True),
                    ("Steal the victim's private keys by brute forcing2256possibilities", False),
                    ('Change the consensus algorithm from PoW to PoS via a soft fork', False),
                    ('Guarantee that the victim always mines valid blocks faster than others', False),
                ]
            },
            {
                'text': 'Why are payments accepted with 0 confirmations generally considered higher risk on public blockchains?',
                'choices': [
                    ('Because an attacker can broadcast a conflicting transaction and exploit propagation timing before any block confirms the payment', True),
                    ('Because transaction fees are always zero at 0 confirmations', False),
                    ('Because 0-confirmation transactions are automatically private by design', False),
                    ('Because cryptographic hashes do not apply until 1 confirmation', False),
                ]
            },
            {
                'text': 'A common mitigation against transaction-spam denial-of-service in fee-based blockchains is:',
                'choices': [
                    ('Using a fee market so that sending many transactions becomes economically costly', True),
                    ('Allowing unlimited block sizes to ensure every spam transaction is included', False),
                    ('Disabling mempools so nodes never store pending transactions', False),
                    ('Replacing all digital signatures with passwords shared publicly', False),
                ]
            },
            {
                'text': 'In a reentrancy vulnerability, which programming mistake most often enables repeated withdrawals?',
                'choices': [
                    ('Performing an external call before updating balances or other critical state variables', True),
                    ('Usingαas a variable name in the code', False),
                    ('Storing balances in an array rather than a mapping', False),
                    ('Using proof-of-stake instead of proof-of-work', False),
                ]
            },
            {
                'text': 'Which ordering best reflects the checks-effects-interactions pattern used to reduce reentrancy risk?',
                'choices': [
                    ('Validate conditions, update internal state, then make external calls', True),
                    ('Make external calls, then validate conditions, then update internal state', False),
                    ('Update internal state, then validate conditions, then make external calls', False),
                    ('Only make external calls and never update internal state', False),
                ]
            },
            {
                'text': 'Why do many modern smart contract languages or compiler versions include built-in checks for integer overflow and underflow?',
                'choices': [
                    ('To prevent arithmetic from wrapping modulo2256, which can bypass validations and create unintended values', True),
                    ('To make hashing functions like SHA-256 produce longer outputs', False),
                    ('To allow negative balances so accounts can borrow without constraints', False),
                    ('To ensure all transactions are confidential by default', False),
                ]
            },
            {
                'text': 'What is the main security risk of usingdelegatecallto an untrusted or attacker-controlled contract?',
                'choices': [
                    ("The callee's code runs with the caller's storage context, enabling storage takeover and privilege escalation", True),
                    ('It makes block confirmations instantaneous', False),
                    ('It guarantees that the called code cannot access any state variables', False),
                    ('It prevents reentrancy by blocking external calls', False),
                ]
            },
            {
                'text': 'Which statement best captures a widely cited difference between zk-SNARKs and zk-STARKs?',
                'choices': [
                    ('zk-STARKs are commonly described as avoiding trusted setup, while zk-SNARKs are often more succinct but may involve trusted setup depending on the construction', True),
                    ('zk-SNARKs are not zero-knowledge, but zk-STARKs are always zero-knowledge', False),
                    ('zk-STARKs require private keys from validators, while zk-SNARKs do not use cryptography', False),
                    ('zk-SNARKs only work for proof-of-work chains, while zk-STARKs only work for proof-of-stake chains', False),
                ]
            },
            {
                'text': 'Privacy-enhancing tools like Tornado Cash use which technology to allow users to prove they have made a deposit without revealing which specific deposit is being withdrawn?',
                'choices': [
                    ('zk-SNARKs (Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge)', True),
                    ('Ring Signatures', False),
                    ('Stealth Addresses', False),
                    ('BGP Hijacking', False),
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
