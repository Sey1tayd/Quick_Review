from django.core.management.base import BaseCommand
from django.db.models import Max
from quiz.models import Course, Session, Question, Choice
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Adds final exam questions for COMP3007'

    def handle(self, *args, **options):
        # Create or get course
        course, created = Course.objects.get_or_create(
            slug='comp3007',
            defaults={'title': 'COMP3007'}
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
                'text': 'Which statement correctly distinguishes arrays and slices in Go?',
                'choices': [
                    ('Slices are fixed-length, while arrays resize automatically when needed.', False),
                    ('Arrays are created with make, while slices must be declared with var only.', False),
                    ('Arrays can only hold strings, while slices can hold any type.', False),
                    ('Arrays have a fixed length, while slices provide a dynamically sized view that can grow (e.g., using append).', True),
                ]
            },
            {
                'text': 'What is the fundamental difference between an array and a slice in Go?',
                'choices': [
                    ('Arrays have a fixed size, while slices are dynamically-sized and provide a flexible view into arrays.', True),
                    ('Arrays can hold multiple data types, whereas slices must be homogeneous.', False),
                    ('Arrays are always passed by reference, while slices are passed by value.', False),
                    ('Only arrays support the \'append\' function for adding new elements.', False),
                ]
            },
            {
                'text': 'Which pattern best represents the standard way to handle returned errors in Go?',
                'choices': [
                    ('Ignore err and rely on the runtime to stop the program if needed.', False),
                    ('Check if err != nil and handle the error before continuing.', True),
                    ('Use try { ... } catch { ... } around every call that returns an error.', False),
                    ('Convert all errors to booleans and return only true/false.', False),
                ]
            },
            {
                'text': 'In a benchmark function, what is the significance of the b.N variable provided by the testing framework?',
                'choices': [
                    ('It is a value adjusted by the framework to run the benchmark loop enough times to get a statistically reliable measurement.', True),
                    ('It represents the total number of CPU cores available for the benchmark.', False),
                    ('It is a constant set to 1,000 to ensure all benchmarks run for the same duration.', False),
                    ('It indicates the number of bytes allocated during a single iteration of the function.', False),
                ]
            },
            {
                'text': 'Which statement about Go benchmark functions is correct?',
                'choices': [
                    ('A benchmark function must return an int representing the number of operations performed.', False),
                    ('A benchmark function name starts with Benchmark, takes *testing.B, and typically loops from i := 0 to b.N.', True),
                    ('The value of b.N is chosen manually and must be hard-coded by the developer.', False),
                    ('Benchmarks are detected only if the function name starts with Test.', False),
                ]
            },
            {
                'text': 'According to Go benchmarking best practices, why is it important to "profile before optimizing"?',
                'choices': [
                    ('To ensure that you are focusing your efforts on actual bottlenecks identified by data rather than guessing.', True),
                    ('To clear the CPU cache so that the optimization runs faster.', False),
                    ('Because the Go compiler will not allow optimizations on code that hasn\'t been profiled.', False),
                    ('To ensure that the code is correctly formatted according to \'go fmt\'.', False),
                ]
            },
            {
                'text': 'Which command is used to execute all benchmark functions in a Go package?',
                'choices': [
                    ('go test -bench=.', True),
                    ('go run benchmark', False),
                    ('go profile -all', False),
                    ('go test -performance', False),
                ]
            },
            {
                'text': 'Which statement accurately describes how Go handles function arguments?',
                'choices': [
                    ('Go is strictly pass-by-value; even pointers are passed by value (the address is copied).', True),
                    ('Go uses pass-by-reference for slices and maps and pass-by-value for basic types.', False),
                    ('Go uses pass-by-reference for all objects to save memory.', False),
                    ('Function arguments are passed by value only if the \'const\' keyword is used.', False),
                ]
            },
            {
                'text': 'Which standard library function is used to check if an error is a specific instance or matches a "sentinel" error type, even if it has been wrapped?',
                'choices': [
                    ('errors.Is()', True),
                    ('errors.As()', False),
                    ('errors.Unwrap()', False),
                    ('errors.New()', False),
                ]
            },
            {
                'text': 'Regarding the build and delivery process, why is Go often considered \'deployment-friendly\' for cloud infrastructure?',
                'choices': [
                    ('It produces static binaries with a simple cross-compilation process, making it easy to ship to various environments.', True),
                    ('It requires a complex set of dynamic libraries to be pre-installed on the host machine.', False),
                    ('Its compiler generates interpreted bytecode that runs on a universal virtual machine.', False),
                    ('It avoids ahead-of-time compilation in favor of just-in-time (JIT) execution.', False),
                ]
            },
            {
                'text': 'When comparing Rust and Go, which statement best captures where each language tends to place complexity?',
                'choices': [
                    ('Go removes the need for any runtime, while Rust depends on a garbage collector.', False),
                    ('Rust pushes many guarantees into compile time, while Go relies more on a runtime (e.g., scheduler and garbage collector) to simplify development.', True),
                    ('Both languages avoid compile-time checking and depend primarily on runtime exceptions.', False),
                    ('Rust and Go are equivalent in how they manage complexity; differences are mostly stylistic.', False),
                ]
            },
            {
                'text': 'Which statement best reflects Go\'s typical approach to code reuse compared to classical inheritance?',
                'choices': [
                    ('Go forbids reusing behavior across types to keep programs simple.', False),
                    ('Go requires every struct to inherit from exactly one base struct.', False),
                    ('Go encourages composition (often via struct embedding) rather than traditional inheritance.', True),
                    ('Go only supports reuse through templates parameterized by types.', False),
                ]
            },
            {
                'text': 'Go encourages composition over inheritance. How is this typically achieved when defining structs?',
                'choices': [
                    ('Through struct embedding, where one struct is included as an anonymous field within another struct.', True),
                    ('By using the \'extends\' keyword to inherit properties from a base struct.', False),
                    ('By defining all structs within a single \'super-package\' that shares memory addresses.', False),
                    ('By using the \'goto\' statement to jump between different struct definitions at runtime.', False),
                ]
            },
            {
                'text': 'Which option best compares the concurrency foundations of Rust and Go?',
                'choices': [
                    ('Rust expresses thread-safety constraints through types and ownership, while Go uses goroutines and channels with runtime scheduling.', True),
                    ('Both languages require writing explicit mutex-based scheduling policies to enable concurrency.', False),
                    ('Rust requires a garbage collector to schedule threads, while Go uses manual memory management to avoid races.', False),
                    ('Go prevents data races in all programs at compile time, while Rust relies on a race detector tool.', False),
                ]
            },
            {
                'text': 'Go is famous for its \'Goroutines.\' How does this concurrency model fundamentally differ from Rust\'s approach to concurrency safety?',
                'choices': [
                    ('Go provides lightweight runtime-scheduled threads and channels, while Rust ensures data race freedom via ownership and trait-based types.', True),
                    ('Go\'s concurrency is managed by the OS kernel, whereas Rust uses a dedicated runtime scheduler for all tasks.', False),
                    ('Rust prevents all forms of concurrent execution, while Go encourages shared-memory access without synchronization.', False),
                    ('There is no difference; both languages use a Global Interpreter Lock (GIL).', False),
                ]
            },
            {
                'text': 'Which pair is most closely associated with Go\'s built-in concurrency model?',
                'choices': [
                    ('Green threads and semaphores', False),
                    ('Fork and join', False),
                    ('Promises and async/await', False),
                    ('Goroutines and channels', True),
                ]
            },
            {
                'text': 'What is the purpose of the iota keyword in Go constant declarations?',
                'choices': [
                    ('It is used to create a sequence of related integer constants, starting from 0.', True),
                    ('It defines a constant that can be modified exactly once during execution.', False),
                    ('It allows a constant to have a dynamic type determined at runtime.', False),
                    ('It serves as a placeholder for null values in constant expressions.', False),
                ]
            },
            {
                'text': 'In Go, which of the following best describes the nature of a struct?',
                'choices': [
                    ('A user-defined type that contains a collection of named fields to group related data together, similar to classes but without inheritance.', True),
                    ('A primitive data type used for high-performance mathematical calculations involving complex numbers.', False),
                    ('A dynamic data structure that automatically inherits all methods from a parent class in a traditional hierarchy.', False),
                    ('A special keyword used only to define global constants and package-level configurations.', False),
                ]
            },
            {
                'text': 'When comparing the primary design motivations of Rust and Go, which of the following best describes the fundamental trade-off between the two languages?',
                'choices': [
                    ('Rust prioritizes compile-time safety and resource control, while Go prioritizes developer simplicity and fast iteration.', True),
                    ('Go eliminates the need for a runtime, whereas Rust relies on a garbage collector for memory management.', False),
                    ('Rust focuses on simplicity for rapid prototyping, while Go is designed primarily for low-level embedded systems.', False),
                    ('Both languages prioritize runtime garbage collection as the only way to achieve memory safety.', False),
                ]
            },
            {
                'text': 'Why would a developer choose to create a custom struct that implements the error interface rather than using errors.New()?',
                'choices': [
                    ('To provide richer information beyond a simple string, such as timestamps or specific failure metadata.', True),
                    ('Because the Go runtime requires custom types for all errors returned from exported functions.', False),
                    ('To bypass the requirement of checking if err != nil.', False),
                    ('Custom error types are processed faster by the garbage collector.', False),
                ]
            },
            {
                'text': 'When using the (database/sql) package, what is the purpose of the (defer db.Close()) statement?',
                'choices': [
                    ('To ensure the database connection is released when the surrounding function returns', True),
                    ('To immediately stop the database server', False),
                    ('To prevent other users from accessing the table', False),
                    ('To delete all data in the database', False),
                ]
            },
            {
                'text': 'A team uses a weighted scoring model to compare Rust and Go across criteria. Which formula correctly computes the total score for a language?',
                'choices': [
                    ('Total = Σ(score) / Σ(weight)', False),
                    ('Total = Σ(weight + score)', False),
                    ('Total = Σ(weight × score)', True),
                    ('Total = Π(weight × score)', False),
                ]
            },
            {
                'text': 'If a function contains multiple \'defer\' statements, in what order are they executed when the function returns?',
                'choices': [
                    ('Last-In, First-Out (LIFO) order.', True),
                    ('First-In, First-Out (FIFO) order.', False),
                    ('Simultaneously via background goroutines.', False),
                    ('Alphabetical order based on the function name being called.', False),
                ]
            },
            {
                'text': 'Which statement best describes the behavior of defer in Go?',
                'choices': [
                    ('Deferred calls are evaluated and executed only at program termination.', False),
                    ('Deferred calls execute only if the function returns nil.', False),
                    ('Deferred calls execute immediately but on a separate goroutine.', False),
                    ('Deferred calls run when the surrounding function returns, and multiple deferred calls execute in last-in-first-out order.', True),
                ]
            },
            {
                'text': 'What is a primary benefit of keeping interfaces small (often with only one or two methods) in Go?',
                'choices': [
                    ('Smaller interfaces are easier to implement, promote better composition, and create more flexible and decoupled code.', True),
                    ('Small interfaces reduce the size of the compiled binary by eliminating unused method signatures.', False),
                    ('Go only supports a maximum of three methods per interface due to memory constraints in the runtime.', False),
                    ('Small interfaces are necessary for the \'go fmt\' tool to correctly align the source code.', False),
                ]
            },
            {
                'text': 'The Go ecosystem is often described as \'batteries included.\' What does this typically mean in comparison to Rust?',
                'choices': [
                    ('Go has a strong, comprehensive standard library for common tasks like networking and web services, whereas Rust relies more on third-party \'crates.\'', True),
                    ('Go requires no external dependencies for any project, while Rust cannot run without a package manager.', False),
                    ('Rust\'s standard library is much larger but harder to use than Go\'s minimal library.', False),
                    ('It refers to Go\'s ability to run on battery-powered mobile devices more efficiently than Rust.', False),
                ]
            },
            {
                'text': 'Which statement best captures a common ecosystem difference between Rust and Go?',
                'choices': [
                    ('Go has no standard library, so most functionality must come from third-party packages.', False),
                    ('Rust often relies on a large crate ecosystem with specialization, while Go emphasizes a strong standard library and uniform patterns.', True),
                    ('Rust forbids third-party dependencies, so projects must be self-contained.', False),
                    ('Both ecosystems are identical because tooling standardization eliminates differences.', False),
                ]
            },
            {
                'text': 'What is the role of the empty interface interface{} in Go?',
                'choices': [
                    ('It can hold a value of any type, making it useful for handling values of unknown concrete type.', True),
                    ('It is a compile-time-only feature and cannot be passed to functions.', False),
                    ('It restricts values to primitive types only.', False),
                    ('It guarantees that the stored value is never nil.', False),
                ]
            },
            {
                'text': 'According to Go best practices, when is it generally appropriate to use panic instead of returning an error?',
                'choices': [
                    ('Only for truly unrecoverable errors where the program cannot meaningfully continue.', True),
                    ('Whenever a file is not found during a standard search.', False),
                    ('As a standard way to signal invalid user input in an HTTP request.', False),
                    ('Whenever a function has more than two return values.', False),
                ]
            },
            {
                'text': 'In modern programming, Rust and Go both discourage silent failures. What is the primary difference in how they structure error propagation?',
                'choices': [
                    ('Rust uses a Result type with the \'?\' operator, while Go uses explicit multiple return values (value, err).', True),
                    ('Rust uses try-catch blocks for all exceptions, while Go uses global error signals.', False),
                    ('Go uses monadic error handling, while Rust relies on sentinel values like -1.', False),
                    ('Both languages use identical syntax for error propagation to ensure interoperability.', False),
                ]
            },
            {
                'text': 'Which statement most accurately compares idiomatic error handling in Rust and Go?',
                'choices': [
                    ('Rust and Go both primarily rely on exceptions for recoverable errors.', False),
                    ('Rust often uses Result<T,E> with explicit propagation (e.g., the ? operator), while Go commonly returns (value, err) and checks if err != nil.', True),
                    ('Go requires pattern matching on errors, while Rust typically ignores errors unless a panic occurs.', False),
                    ('Both languages guarantee that all errors are automatically logged with full context.', False),
                ]
            },
            {
                'text': 'In Go, a type satisfies the built-in error interface if it implements which method?',
                'choices': [
                    ('Code() int', False),
                    ('Error() string', True),
                    ('ToString() string', False),
                    ('Message() string', False),
                ]
            },
            {
                'text': 'When using fmt.Errorf, which formatting verb must be used to wrap an existing error so that it can be later extracted or inspected?',
                'choices': [
                    ('%w', True),
                    ('%v', False),
                    ('%s', False),
                    ('%e', False),
                ]
            },
            {
                'text': 'Which formatting verb is used with fmt.Errorf to wrap an existing error in Go?',
                'choices': [
                    ('%E', False),
                    ('%w', True),
                    ('%r', False),
                    ('%e', False),
                ]
            },
            {
                'text': 'Which statement best reflects Go\'s general philosophy for handling errors?',
                'choices': [
                    ('Errors are ignored unless the runtime detects a fatal condition.', False),
                    ('Errors are handled primarily using try/catch blocks.', False),
                    ('Errors are returned as normal values and checked explicitly by the caller.', True),
                    ('Errors automatically propagate upward until they are handled globally.', False),
                ]
            },
            {
                'text': 'When is errors.As(err, &target) most appropriate?',
                'choices': [
                    ('When you want to compare errors by pointer identity only.', False),
                    ('When you want to format an error message with fmt.Errorf.', False),
                    ('When you want to suppress all errors and return nil.', False),
                    ('When you want to check whether an error (possibly wrapped) can be treated as a specific custom error type.', True),
                ]
            },
            {
                'text': 'What is the main purpose of errors.Is(err, target) in Go?',
                'choices': [
                    ('To unwrap errors and always return the original root cause only.', False),
                    ('To convert any error into a string without calling Error().', False),
                    ('To test whether err matches a target error (including through wrapped errors).', True),
                    ('To automatically recover from a panic and continue execution.', False),
                ]
            },
            {
                'text': 'In Go, how is a variable, function, or constant made available (exported) to other packages?',
                'choices': [
                    ('By starting the identifier\'s name with an uppercase letter.', True),
                    ('By using the \'public\' keyword before the declaration.', False),
                    ('By declaring it within the \'main\' package.', False),
                    ('By adding an underscore at the end of the name.', False),
                ]
            },
            {
                'text': 'In a minimal Go HTTP server without a third-party router, which approach is commonly used to extract a simple parameter from the request path (e.g., an ID after a fixed prefix)?',
                'choices': [
                    ('Use r.Body.Path which stores URL segments as a list.', False),
                    ('Call r.ParseForm() to populate path variables automatically.', False),
                    ('Read r.URL.Path and slice/parse it relative to a known prefix (with validation).', True),
                    ('Use fmt.Scan() to scan the URL from standard input.', False),
                ]
            },
            {
                'text': 'Which option lists a valid set of common for loop forms supported by Go?',
                'choices': [
                    ('Classic form, do-while form, foreach keyword form, and generator-based form.', False),
                    ('Only the classic three-part form; other loops are not supported.', False),
                    ('While-only form and repeat-until form only.', False),
                    ('Classic three-part form, condition-only form, infinite loop form, and range-based iteration.', True),
                ]
            },
            {
                'text': 'Which of the following statements is true regarding function signatures and return values in Go?',
                'choices': [
                    ('Functions can return multiple values, and parameters of the same type can share a single type declaration.', True),
                    ('Functions can only return a single value or a pointer to a struct.', False),
                    ('Every function must return an error as its last return value.', False),
                    ('Return types are inferred automatically and do not need to be specified in the signature.', False),
                ]
            },
            {
                'text': 'In Go, what is the primary behavior of a panic when it is triggered?',
                'choices': [
                    ('It stops normal execution, runs any deferred functions in the current goroutine, and terminates the program if not recovered.', True),
                    ('It immediately crashes the CPU to prevent any further memory corruption.', False),
                    ('It acts as a breakpoint that allows for real-time debugging without stopping the program flow.', False),
                    ('It logs an error message to a file but allows the current function to continue executing normally.', False),
                ]
            },
            {
                'text': 'In Go, what best defines a block?',
                'choices': [
                    ('The set of all imported packages in a program.', False),
                    ('Any file that belongs to a Go package, regardless of braces.', False),
                    ('A sequence of declarations and statements enclosed by matching braces { }.', True),
                    ('A special syntax used only for loops and conditionals.', False),
                ]
            },
            {
                'text': 'In the Go programming language, which of the following statements correctly describes the visibility of variables across nested blocks?',
                'choices': [
                    ('Inner blocks can access variables declared in outer blocks, but outer blocks cannot access variables from inner blocks.', True),
                    ('Variables are globally accessible once declared within any function block.', False),
                    ('Inner blocks are isolated and cannot see variables declared in the surrounding outer scope.', False),
                    ('Outer blocks can access variables from inner blocks as long as the inner block has finished execution.', False),
                ]
            },
            {
                'text': 'Which command is commonly used to run tests in a Go module or package?',
                'choices': [
                    ('go install test', False),
                    ('go build -test', False),
                    ('go test', True),
                    ('go run test', False),
                ]
            },
            {
                'text': 'Which statement best describes the fundamental philosophy of error handling in the Go programming language?',
                'choices': [
                    ('Errors are treated as values that are returned as normal return values from functions, encouraging explicit checking.', True),
                    ('Errors are handled using try/catch blocks and exceptions to separate error logic from program flow.', False),
                    ('All errors result in an immediate panic to ensure that the program does not run with an invalid state.', False),
                    ('Errors are globally managed by a background goroutine to minimize boilerplate code in business logic.', False),
                ]
            },
            {
                'text': 'Which statement best describes the Go programming language?',
                'choices': [
                    ('It is a purely functional language with lazy evaluation by default.', False),
                    ('It is a statically typed, compiled language designed with simplicity and efficiency in mind.', True),
                    ('It is a language that requires a virtual machine to execute compiled bytecode.', False),
                    ('It is a dynamically typed scripting language that relies on an interpreter.', False),
                ]
            },
            {
                'text': 'Which organization originally developed the Go programming language, and who were its primary creators?',
                'choices': [
                    ('Google; developed by Robert Griesemer, Rob Pike, and Ken Thompson', True),
                    ('Microsoft; developed by Anders Hejlsberg', False),
                    ('Apple; developed by Chris Lattner', False),
                    ('Sun Microsystems; developed by James Gosling', False),
                ]
            },
            {
                'text': 'Which of the following describes the \'while\' loop equivalent in Go?',
                'choices': [
                    ('A \'for\' loop with only a single condition statement.', True),
                    ('The \'while\' keyword followed by a boolean expression.', False),
                    ('The \'do-while\' keyword combination.', False),
                    ('A \'range\' loop applied to a boolean channel.', False),
                ]
            },
            {
                'text': 'For a Go program to produce an executable that can be run directly, which package typically contains the entry point?',
                'choices': [
                    ('runtime', False),
                    ('init', False),
                    ('main', True),
                    ('start', False),
                ]
            },
            {
                'text': 'Which Go standard-library package is most commonly used to build HTTP clients and servers?',
                'choices': [
                    ('net/tcp', False),
                    ('http/server', False),
                    ('web/http', False),
                    ('net/http', True),
                ]
            },
            {
                'text': 'In Go, testing is considered a "first-class citizen." What does this mean for developers building Go applications?',
                'choices': [
                    ('The testing package is built-in, meaning no external testing frameworks are strictly required to write and run tests.', True),
                    ('Tests must be written in a separate, specialized testing language before being compiled into Go.', False),
                    ('All Go functions must have a corresponding test function or the compiler will reject the code.', False),
                    ('Testing is only available for package-level variables and cannot be used for local function logic.', False),
                ]
            },
            {
                'text': 'Which command in the Go toolchain is specifically used to format source code according to standard style conventions?',
                'choices': [
                    ('go fmt', True),
                    ('go build', False),
                    ('go mod', False),
                    ('go clean', False),
                ]
            },
            {
                'text': 'Which of the following is considered a primary advantage of using Go for web development according to standard industry practices?',
                'choices': [
                    ('Built-in concurrency and low resource usage', True),
                    ('Strict requirement for heavy external frameworks', False),
                    ('Lack of standard library support for HTTP', False),
                    ('Slow execution speed due to interpreted nature', False),
                ]
            },
            {
                'text': 'In Go web programming, what must a type implement to be used as an HTTP handler?',
                'choices': [
                    ('A method ServeHTTP(w http.ResponseWriter, r *http.Request).', True),
                    ('A method RunHTTP() that starts the server automatically.', False),
                    ('A method Handle(w, r) with any parameter types.', False),
                    ('A function named mainHandler() declared in package main.', False),
                ]
            },
            {
                'text': 'In Go, an \'if\' statement can include an initialization statement, such as if err := f(); err != nil. What is the scope of the variable err?',
                'choices': [
                    ('The variable err is only visible within the \'if\', \'else if\', and \'else\' blocks of that statement.', True),
                    ('The variable err remains in scope for the rest of the function.', False),
                    ('The variable err is a package-level global variable.', False),
                    ('The variable err is only visible in the condition check and not the block body.', False),
                ]
            },
            {
                'text': 'Which statement about variables declared in an if initialization statement is true?',
                'choices': [
                    ('They become package-level variables for the rest of the program.', False),
                    ('They are visible after the if statement finishes executing.', False),
                    ('They are visible only within the corresponding if/else blocks created by that statement.', True),
                    ('They must be declared using var, not :=.', False),
                ]
            },
            {
                'text': 'How does a type implement an interface in Go?',
                'choices': [
                    ('By embedding the interface type as an anonymous field in the struct.', False),
                    ('By registering the type in a runtime interface table.', False),
                    ('By providing methods matching the interface; no explicit declaration of intent is required.', True),
                    ('By writing implements InterfaceName after the type definition.', False),
                ]
            },
            {
                'text': 'Which prefix indicates a hexadecimal integer literal in Go?',
                'choices': [
                    ('0o (e.g., 0o52)', False),
                    ('0b (e.g., 0b101010)', False),
                    ('0x (e.g., 0x2A)', True),
                    ('0d (e.g., 0d42)', False),
                ]
            },
            {
                'text': 'What does an interface define in Go?',
                'choices': [
                    ('A set of method signatures that a type can satisfy by implementing those methods.', True),
                    ('A required base class that all structs must extend.', False),
                    ('A module system for importing packages.', False),
                    ('A concrete data layout with named fields.', False),
                ]
            },
            {
                'text': 'How does a concrete type in Go implement a specific interface?',
                'choices': [
                    ('A type implements an interface implicitly by implementing all the method signatures defined in the interface; no explicit declaration is needed.', True),
                    ('The type must use the \'implements\' keyword followed by the interface name in its declaration.', False),
                    ('Interfaces are automatically implemented by all types that are defined within the same package.', False),
                    ('A type must be cast to the interface type at the time of its definition using the interface{} syntax.', False),
                ]
            },
            {
                'text': 'When integrating components written in different languages, which tradeoff is commonly considered?',
                'choices': [
                    ('In-process FFI can improve performance but increases boundary complexity, while process/RPC boundaries can simplify operations at the cost of overhead.', True),
                    ('FFI is always safer than RPC because it avoids network communication.', False),
                    ('Interoperability never affects security; only cryptographic choices matter.', False),
                    ('RPC is always faster than FFI because it runs in parallel by default.', False),
                ]
            },
            {
                'text': 'Given the Go constant block below, what are the values of A, B, and C?\n\nconst (\n  A = iota\n  B\n  C\n)',
                'choices': [
                    ('0, 1, 2', True),
                    ('1, 2, 3', False),
                    ('0, 0, 0', False),
                    ('1, 1, 1', False),
                ]
            },
            {
                'text': 'When receiving JSON in an HTTP request body in Go, which approach is most idiomatic?',
                'choices': [
                    ('Use fmt.Fscan(r.Body, &v) to parse JSON automatically.', False),
                    ('Call r.ParseForm() and read JSON from r.PostForm.', False),
                    ('Use json.NewDecoder(r.Body).Decode(&v) and handle decoding errors explicitly.', True),
                    ('Set w.Header().Set(\'Content-Type\',\'application/json\') before decoding the request body.', False),
                ]
            },
            {
                'text': 'When working with JSON in Go, which mechanism is typically used to map a JSON field named \'age\' to a struct field named \'Age\'?',
                'choices': [
                    ('Struct tags, such as \'json:"age"\'', True),
                    ('Manual string parsing', False),
                    ('Global configuration variables', False),
                    ('Pointer aliasing', False),
                ]
            },
            {
                'text': 'Go utilizes lexical scoping. What is the primary implication of this for anonymous functions or closures?',
                'choices': [
                    ('A function can \'see\' and access variables in the scope where it was defined, even after the outer function has returned.', True),
                    ('The scope of a variable is determined at runtime based on the calling stack.', False),
                    ('Variables are only visible to functions if they are passed explicitly as arguments.', False),
                    ('Anonymous functions cannot access variables from the outer scope to prevent memory leaks.', False),
                ]
            },
            {
                'text': 'What does it mean that Go uses lexical scoping?',
                'choices': [
                    ('The scope of an identifier is determined by its location in the source code and can be resolved at compile time.', True),
                    ('Only variables inside functions participate in scoping rules.', False),
                    ('Identifiers are resolved based on the most recent runtime call stack frame.', False),
                    ('All identifiers are globally visible once imported.', False),
                ]
            },
            {
                'text': 'In Go, map keys must be of a type that is comparable (i.e., it supports equality checks). Which type below can be used as a map key?',
                'choices': [
                    ('func() (function type)', False),
                    ('map[string]int', False),
                    ('[]int (slice of int)', False),
                    ('string', True),
                ]
            },
            {
                'text': 'Which built-in function is used to initialize a map and what is the characteristic of map keys?',
                'choices': [
                    ('Maps are initialized with \'make()\', and keys can be any type that is comparable.', True),
                    ('Maps are initialized with \'new()\', and keys must be strings.', False),
                    ('Maps are initialized with \'init()\', and keys must be numeric.', False),
                    ('Maps are initialized with \'alloc()\', and keys can be any type including slices.', False),
                ]
            },
            {
                'text': 'In Go, what is a method?',
                'choices': [
                    ('A function that can only be defined on struct types.', False),
                    ('A function that must be declared inside a struct body.', False),
                    ('A function that is automatically parallelized across all CPU cores.', False),
                    ('A function with a receiver, associating it with a specific named type.', True),
                ]
            },
            {
                'text': 'Which command option is commonly used to report test coverage for Go code?',
                'choices': [
                    ('Run go test -cover to see a coverage percentage.', True),
                    ('Coverage is only available in third-party frameworks, not the Go toolchain.', False),
                    ('Run go test -optimize to measure coverage and speed.', False),
                    ('Run go coverage to generate an automatic report.', False),
                ]
            },
            {
                'text': 'Which Go toolchain command is used to view the percentage of code covered by existing tests?',
                'choices': [
                    ('go test -cover', True),
                    ('go tool verify', False),
                    ('go check -percentage', False),
                    ('go coverage -run', False),
                ]
            },
            {
                'text': 'How do Rust and Go differ in their approach to ensuring memory safety?',
                'choices': [
                    ('Rust uses an ownership and borrowing system at compile time, while Go uses a runtime garbage collector.', True),
                    ('Rust relies on manual memory management (malloc/free), while Go uses reference counting.', False),
                    ('Go requires explicit lifetimes in function signatures, whereas Rust manages memory via a background scheduler.', False),
                    ('Both languages use garbage collection, but Rust allows developers to disable it for specific blocks of code.', False),
                ]
            },
            {
                'text': 'Which option correctly compares the default memory management models of Rust and Go?',
                'choices': [
                    ('Both languages avoid garbage collection by using reference counting as the default.', False),
                    ('Rust enforces ownership and borrowing rules at compile time, while Go primarily uses garbage collection at runtime.', True),
                    ('Rust and Go both require manual memory management with explicit free calls.', False),
                    ('Go enforces lifetimes in function signatures, while Rust relies on a stop-the-world garbage collector.', False),
                ]
            },
            {
                'text': 'Which statement accurately reflects how methods are defined in the Go programming language?',
                'choices': [
                    ('Methods are functions associated with a particular type and can be defined on any named type, not just structs.', True),
                    ('Methods must be defined exclusively within the curly braces of a struct definition.', False),
                    ('Methods are only applicable to pointer types and cannot be used with value types.', False),
                    ('Methods in Go require a \'virtual\' keyword to allow for polymorphism.', False),
                ]
            },
            {
                'text': 'What is the main idea of middleware in Go HTTP servers?',
                'choices': [
                    ('A function that wraps an http.Handler to run logic before and/or after the next handler.', True),
                    ('A special goroutine that schedules requests using priority.', False),
                    ('A compiler feature that injects code into binaries during linking.', False),
                    ('A database trigger that runs whenever a row is updated.', False),
                ]
            },
            {
                'text': 'In the context of Go web servers, what is the standard pattern for a middleware function?',
                'choices': [
                    ('A function that takes an (http.Handler) and returns a new (http.Handler)', True),
                    ('A function that terminates the server immediately', False),
                    ('A direct connection to the database driver', False),
                    ('A method that only handles 404 errors', False),
                ]
            },
            {
                'text': 'Why are interfaces considered essential for effective unit testing and mocking in Go?',
                'choices': [
                    ('They allow developers to swap real external dependencies (like databases) with mock implementations during testing.', True),
                    ('They are the only way to access private variables within a test file.', False),
                    ('They automatically generate test data for every possible input of a function.', False),
                    ('They prevent the compiler from optimizing away the test functions.', False),
                ]
            },
            {
                'text': 'Which approach is most idiomatic for mocking an external dependency in Go?',
                'choices': [
                    ('Use class inheritance and override methods in a subclass for tests.', False),
                    ('Only use global variables because they are easiest to replace.', False),
                    ('Define an interface for the dependency and provide a fake or mock implementation for tests.', True),
                    ('Disable type checking so any object can be used as a mock at runtime.', False),
                ]
            },
            {
                'text': 'Which scenario most idiomatically motivates multiple return values in Go?',
                'choices': [
                    ('Allowing functions to implicitly change global variables without side effects.', False),
                    ('Guaranteeing that functions always mutate their arguments in-place.', False),
                    ('Replacing the need for control structures like if and switch.', False),
                    ('Returning a computed result along with an error value to indicate success or failure.', True),
                ]
            },
            {
                'text': 'What is a characteristic of "Named Return Values" in Go functions?',
                'choices': [
                    ('They are initialized to their zero values at the start of the function and allow the use of a "naked" return.', True),
                    ('They prevent the function from returning more than one value.', False),
                    ('They are only used for documentation and cannot be modified within the function.', False),
                    ('They require the \'return\' keyword to be followed by the variable names in every instance.', False),
                ]
            },
            {
                'text': 'In Go, what happens when you try to assign a value of type int32 directly to a variable of type int64 without conversion?',
                'choices': [
                    ('It compiles but panics at runtime.', False),
                    ('It compiles and automatically widens the value to int64.', False),
                    ('It fails to compile because Go does not allow implicit type conversion in assignments.', True),
                    ('It compiles, but the value becomes zero due to overflow rules.', False),
                ]
            },
            {
                'text': 'Using a weighted scoring model for a project where simplicity > safety and fast iteration > safety, which language is likely to be the preferred choice?',
                'choices': [
                    ('Go, because it optimizes for a simple mental model and fast iteration.', True),
                    ('Rust, because it provides the highest possible safety guarantees regardless of complexity.', False),
                    ('Neither, as simplicity and safety are mutually exclusive in systems programming.', False),
                    ('C++, because it ignores both simplicity and safety constraints.', False),
                ]
            },
            {
                'text': 'Which statement about panic in Go is accurate?',
                'choices': [
                    ('It automatically continues execution after logging the message.', False),
                    ('It is the recommended default alternative to returning errors from functions.', False),
                    ('It stops normal execution of the current goroutine and runs deferred functions; if not recovered, the program terminates.', True),
                    ('It only affects the current function and never impacts callers.', False),
                ]
            },
            {
                'text': 'When evaluating performance, what is a common factor that might cause \'tail latency\' issues in Go applications that is largely absent in Rust?',
                'choices': [
                    ('Garbage collection (GC) pauses and runtime scheduling overhead.', True),
                    ('Lack of support for asynchronous I/O.', False),
                    ('The requirement to compile code at runtime.', False),
                    ('Inefficient integer arithmetic operations.', False),
                ]
            },
            {
                'text': 'Why might you choose a pointer receiver for a method in Go?',
                'choices': [
                    ('To allow the method to modify the receiver\'s underlying value (and to avoid copying large structs).', True),
                    ('Because pointer receivers are required for all interfaces.', False),
                    ('To make the method a generic function over T and *T.', False),
                    ('Because value receivers cannot read fields of the receiver.', False),
                ]
            },
            {
                'text': 'Which statement about Go\'s predeclared identifiers (e.g., int, true, make, nil) is correct?',
                'choices': [
                    ('They can be safely redeclared inside a function because function scope is isolated.', False),
                    ('They must be imported from a special standard package.', False),
                    ('They are only visible in the main package.', False),
                    ('They are available throughout Go code and cannot be redeclared in another block without causing a compilation error.', True),
                ]
            },
            {
                'text': 'Which pair is most appropriate for handling typical HTML form submissions in a Go HTTP handler?',
                'choices': [
                    ('Use template.Execute to parse and validate the form fields.', False),
                    ('Use sql.Open to read form fields from the database.', False),
                    ('Call r.ParseForm() and then read values using r.FormValue(\'field\') (or r.PostForm).', True),
                    ('Call json.NewDecoder(r.Body).Decode(...) for all forms.', False),
                ]
            },
            {
                'text': 'Which sequence best matches a typical Go profiling workflow?',
                'choices': [
                    ('Run go test -cover and it automatically opens an interactive pprof server.', False),
                    ('Run tests with a profile flag (e.g., go test -cpuprofile cpu.prof) and then analyze it using go tool pprof (optionally with a web UI).', True),
                    ('Use go run to generate cpu.prof; pprof reads it only during compilation.', False),
                    ('Profiling is unnecessary if the benchmark average time per operation T/N is small.', False),
                ]
            },
            {
                'text': 'If a developer wants to identify which parts of their Go code are consuming the most execution time, which type of profiling should they use?',
                'choices': [
                    ('CPU Profiling', True),
                    ('Memory Profiling', False),
                    ('Block Profiling', False),
                    ('Goroutine Profiling', False),
                ]
            },
            {
                'text': 'Which description best matches a struct in Go?',
                'choices': [
                    ('A built-in reference type used only for key-value lookup.', False),
                    ('A mechanism for classical inheritance and method overriding.', False),
                    ('A collection that can only store values of type interface{}.', False),
                    ('A user-defined type that groups related data as named fields.', True),
                ]
            },
            {
                'text': 'According to Go best practices, why should you be consistent with receiver types for a given named type?',
                'choices': [
                    ('Consistency ensures a predictable method set and prevents confusion about which methods modify the object and which do not.', True),
                    ('Mixing receiver types is prohibited by the Go compiler and will result in a "stray pointer" error.', False),
                    ('Consistent receivers are required to allow the garbage collector to identify unused structs.', False),
                    ('Using only value receivers is mandatory for any code intended to run on 64-bit systems.', False),
                ]
            },
            {
                'text': 'Under what condition does recover() work as intended in Go?',
                'choices': [
                    ('It only works in the main package and is ignored elsewhere.', False),
                    ('It can be called anywhere to prevent any future panics.', False),
                    ('It must be called inside a deferred function to regain control after a panic.', True),
                    ('It must be called before panic to disable it.', False),
                ]
            },
            {
                'text': 'Where is the only effective place to call the recover function to regain control of a panicking goroutine?',
                'choices': [
                    ('Inside a deferred function.', True),
                    ('In the main initialization block of the package.', False),
                    ('Inside an if-statement immediately following the potential panic point.', False),
                    ('Within a separate background goroutine designated for monitoring.', False),
                ]
            },
            {
                'text': 'According to RESTful design principles, which HTTP method is most appropriate for retrieving a specific resource?',
                'choices': [
                    ('GET', True),
                    ('POST', False),
                    ('DELETE', False),
                    ('PUT', False),
                ]
            },
            {
                'text': 'Which choice best matches a common RESTful design guideline?',
                'choices': [
                    ('Return HTTP 200 for every response regardless of errors.', False),
                    ('Store server session state inside URLs to keep endpoints stateless.', False),
                    ('Use HTTP methods (GET, POST, PUT, DELETE) to operate on resource-oriented URLs.', True),
                    ('Use a single POST endpoint for all operations to simplify clients.', False),
                ]
            },
            {
                'text': 'Which component is commonly used in Go to route incoming HTTP requests by URL path to different handlers?',
                'choices': [
                    ('A net.Listener that automatically dispatches based on file names.', False),
                    ('A database/sql driver registry.', False),
                    ('An http.ServeMux (e.g., created with http.NewServeMux()).', True),
                    ('A sync.Mutex that guards URL lookups.', False),
                ]
            },
            {
                'text': 'Which statement best reflects how Rust and Go typically prevent certain bug classes?',
                'choices': [
                    ('Neither language provides meaningful safety advantages; security depends only on encryption libraries.', False),
                    ('Go guarantees data-race freedom at compile time, while Rust allows races unless you use special tools.', False),
                    ('Rust prevents only logic bugs, while Go prevents only memory bugs.', False),
                    ('Rust prevents many memory and data-race errors by construction in safe code, while Go often relies on runtime behavior and tooling to detect or mitigate issues.', True),
                ]
            },
            {
                'text': 'Which scope rule is correct for nested blocks in Go?',
                'choices': [
                    ('Inner blocks can access identifiers from outer blocks, but outer blocks cannot access identifiers declared in inner blocks.', True),
                    ('All variables become inaccessible when entering an inner block.', False),
                    ('Variables declared in any block are visible everywhere in the file.', False),
                    ('Outer blocks can access variables from inner blocks after the inner block ends.', False),
                ]
            },
            {
                'text': 'What is a sentinel error in Go?',
                'choices': [
                    ('An error created only inside panic calls.', False),
                    ('An error that is automatically retried until it disappears.', False),
                    ('An error that must contain a field Code to be valid.', False),
                    ('A predefined error value used to represent an expected error condition for comparison and handling.', True),
                ]
            },
            {
                'text': 'What are "sentinel errors" in the context of Go programming?',
                'choices': [
                    ('Predefined error variables exported by a package for expected error conditions, such as io.EOF.', True),
                    ('Errors that are automatically generated by the operating system kernel.', False),
                    ('Private error types that cannot be inspected by other packages.', False),
                    ('Errors that only occur when a program is running in "Sentinel Mode" for high availability.', False),
                ]
            },
            {
                'text': 'What is the primary role of an (http.ServeMux) in a Go web application?',
                'choices': [
                    ('It acts as an HTTP request multiplexer to route incoming requests to handlers', True),
                    ('It manages the connection pool for a SQL database', False),
                    ('It compiles HTML templates into binary format', False),
                    ('It encrypts outgoing JSON responses', False),
                ]
            },
            {
                'text': 'Which Go package is commonly used to render server-side HTML templates safely?',
                'choices': [
                    ('net/template', False),
                    ('fmt/template', False),
                    ('text/html', False),
                    ('html/template', True),
                ]
            },
            {
                'text': 'Which response header is typically set before returning JSON from a Go HTTP handler?',
                'choices': [
                    ('Server: json', False),
                    ('Content-Type: application/json', True),
                    ('Accept: application/json', False),
                    ('Content-Encoding: json', False),
                ]
            },
            {
                'text': 'Which statement about the := short variable declaration in Go is correct?',
                'choices': [
                    ('It can only be used inside functions and requires an initializer value.', True),
                    ('It declares constants and enforces immutability.', False),
                    ('It always requires an explicit type annotation on the left-hand side.', False),
                    ('It can be used to declare global variables without initialization.', False),
                ]
            },
            {
                'text': 'Which Go standard-library function is commonly used to convert a decimal string like \'42\' into an integer while also returning an error value?',
                'choices': [
                    ('strconv.Atoi', True),
                    ('math.ParseInt', False),
                    ('strings.Int', False),
                    ('fmt.Sprintf', False),
                ]
            },
            {
                'text': 'When a struct type embeds another struct type, what is the typical effect?',
                'choices': [
                    ('The embedded type becomes a superclass and enables method overriding.', False),
                    ('The embedded type is copied at compile time into every function that uses it.', False),
                    ('The embedded type must always be a pointer, not a value.', False),
                    ('The embedded type\'s fields and methods can be promoted for convenient access via the outer type.', True),
                ]
            },
            {
                'text': 'What is an advantage of using named-field struct literals in Go?',
                'choices': [
                    ('Fields are assigned by name, improving readability and reducing errors from field-order changes.', True),
                    ('It prevents taking the address of the created struct.', False),
                    ('It forces all fields to be immutable after initialization.', False),
                    ('It automatically allocates the struct in shared memory across goroutines.', False),
                ]
            },
            {
                'text': 'In Go tests, what is a key difference between t.Error(...) and t.Fatal(...)?',
                'choices': [
                    ('t.Fatal can only be used in benchmarks.', False),
                    ('They are equivalent; the names differ only for style.', False),
                    ('t.Fatal marks the test failed and stops execution immediately, while t.Error marks failure but continues.', True),
                    ('t.Error stops the test immediately, while t.Fatal continues.', False),
                ]
            },
            {
                'text': 'What is the main idea behind table-driven tests in Go?',
                'choices': [
                    ('Run tests only for values where b.N > 0.', False),
                    ('Use HTML tables to display test results in the console.', False),
                    ('Store tests in a database table and query them at runtime.', False),
                    ('Define a list of test cases (inputs and expected outputs) and loop over them to run the same logic consistently.', True),
                ]
            },
            {
                'text': 'What is the main advantage of using table-driven tests in Go?',
                'choices': [
                    ('They provide a clean way to test multiple sets of inputs and expected outputs within a single test function.', True),
                    ('They allow tests to be exported into external database tables for easier management.', False),
                    ('They reduce the compilation time of the test suite by up to 50%.', False),
                    ('They are required for any function that returns more than three values.', False),
                ]
            },
            {
                'text': 'In latency-sensitive services, which factor is commonly cited when comparing Go and Rust?',
                'choices': [
                    ('Go has no runtime, so tail latency is determined only by CPU cache effects.', False),
                    ('Tail latency depends only on T and U values chosen at build time.', False),
                    ('Go can have tail-latency effects from garbage collection and scheduling, while Rust often aims for more predictable memory behavior (depending on design).', True),
                    ('Rust always has worse tail latency because it lacks a runtime scheduler.', False),
                ]
            },
            {
                'text': 'Which method is used to merge a Go data structure with an HTML template to produce the final output for the client?',
                'choices': [
                    ('Execute', True),
                    ('Parse', False),
                    ('New', False),
                    ('Stringify', False),
                ]
            },
            {
                'text': 'What are the naming and parameter requirements for a standard unit test function in Go?',
                'choices': [
                    ('The function name must start with \'Test\' and it must take a single parameter of type \'*testing.T\'.', True),
                    ('The function name must end with \'_test\' and it must return a boolean value.', False),
                    ('The function must be named \'main_test\' and accept a slice of strings as arguments.', False),
                    ('The function name must be all lowercase \'test\' and take a pointer to the package block.', False),
                ]
            },
            {
                'text': 'Which requirement is necessary for a basic Go test function to be recognized by the test runner?',
                'choices': [
                    ('The function name ends with Test and returns an error.', False),
                    ('The function must be inside package main.', False),
                    ('The function must print \'PASS\' to standard output.', False),
                    ('The function name starts with Test and it takes a parameter of type *testing.T.', True),
                ]
            },
            {
                'text': 'Which tool from the standard library is specifically designed to record and inspect the response of an HTTP handler during unit testing?',
                'choices': [
                    ('httptest.ResponseRecorder', True),
                    ('fmt.Println', False),
                    ('log.Fatal', False),
                    ('os.Stdout', False),
                ]
            },
            {
                'text': 'Which package is commonly used to test HTTP handlers in Go without running a real network server?',
                'choices': [
                    ('net/http/cgi', False),
                    ('os/exec', False),
                    ('runtime/debug', False),
                    ('net/http/httptest', True),
                ]
            },
            {
                'text': 'What is the unique characteristic of the empty interface interface{} in Go?',
                'choices': [
                    ('It defines zero methods and can therefore hold values of any type.', True),
                    ('It is a restricted interface that prevents any data from being stored within it for security purposes.', False),
                    ('It acts as a destructor to clear memory when a struct goes out of scope.', False),
                    ('It is used to define abstract classes that cannot be instantiated.', False),
                ]
            },
            {
                'text': 'What is the structure of the built-in error interface in Go?',
                'choices': [
                    ('An interface with a single method: Error() string', True),
                    ('A struct containing an error code and a message string', False),
                    ('An interface with two methods: Error() string and Code() int', False),
                    ('A pointer type that references a system-level error buffer', False),
                ]
            },
            {
                'text': 'To satisfy the (http.Handler) interface in Go, a type must implement which of the following methods?',
                'choices': [
                    ('ServeHTTP(ResponseWriter, *Request)', True),
                    ('HandleRequest(ResponseWriter, *Request)', False),
                    ('Process(ResponseWriter, *Request)', False),
                    ('Listen(string, Handler)', False),
                ]
            },
            {
                'text': 'In the Go standard library, which package provides the core implementations for both HTTP clients and servers?',
                'choices': [
                    ('net/http', True),
                    ('web/http', False),
                    ('io/network', False),
                    ('net/url', False),
                ]
            },
            {
                'text': 'What is the primary function of the go tool pprof command?',
                'choices': [
                    ('To analyze and visualize profiling data, such as generating graphs or interactive web UIs to inspect performance.', True),
                    ('To automatically rewrite slow code using more efficient algorithms.', False),
                    ('To deploy Go binaries to a production server with optimized performance flags.', False),
                    ('To check for syntax errors in the benchmark functions.', False),
                ]
            },
            {
                'text': 'Which of the following is true regarding the \'Universe Block\' in Go?',
                'choices': [
                    ('It contains all predeclared identifiers like int, true, and make, which cannot be redeclared in other blocks.', True),
                    ('It is a local block created within every \'main\' function.', False),
                    ('It only contains user-defined global variables.', False),
                    ('It must be explicitly imported using the \'universe\' keyword.', False),
                ]
            },
            {
                'text': 'What does the \'comma ok\' form of a type assertion accomplish?',
                'choices': [
                    ('It safely checks whether an interface value holds a specific concrete type, returning the value and a boolean success flag.', True),
                    ('It guarantees the assertion succeeds and removes the need for error handling.', False),
                    ('It forces the interface value to become interface{}.', False),
                    ('It converts between numeric types automatically without an explicit cast.', False),
                ]
            },
            {
                'text': 'In Go, what is the purpose of the "comma ok" idiom when performing a type assertion like v, ok := i.(T)?',
                'choices': [
                    ('It provides a safe way to test whether an interface value holds a specific concrete type without causing a panic if the assertion fails.', True),
                    ('It is used to verify that a variable is not nil before it is passed to a function.', False),
                    ('It converts a floating-point number to an integer while checking for precision loss.', False),
                    ('It is a requirement for all switch statements to ensure that a default case is always present.', False),
                ]
            },
            {
                'text': 'How does Go handle type conversion between different numeric types, such as assigning an int32 to an int64?',
                'choices': [
                    ('Automatic conversion is not allowed; it requires an explicit conversion using the T(v) syntax.', True),
                    ('It performs automatic "widening" conversions but requires explicit "narrowing" conversions.', False),
                    ('Go is dynamically typed and handles these assignments automatically at runtime.', False),
                    ('Assignments between signed integers of different sizes are performed automatically by the compiler.', False),
                ]
            },
            {
                'text': 'What is the primary purpose of a type switch in Go?',
                'choices': [
                    ('To automatically infer generic types for a function at runtime.', False),
                    ('To convert any value into a different type without explicit conversion.', False),
                    ('To enforce that all variables in a function share the same static type.', False),
                    ('To branch logic based on the dynamic concrete type stored in an interface value.', True),
                ]
            },
            {
                'text': 'What distinguishes a type switch from a regular switch statement in Go?',
                'choices': [
                    ('A type switch compares types rather than values, using the syntax switch v := i.(type) to determine the concrete type of an interface.', True),
                    ('A type switch is only used for determining if a variable is public or private.', False),
                    ('A type switch is a performance optimization that only works with boolean values.', False),
                    ('A type switch allows the program to jump to a different package based on the CPU architecture.', False),
                ]
            },
            {
                'text': 'Which feature of the Rust type system allows it to encode complex invariants and reduce misuse paths compared to the minimalist approach of Go?',
                'choices': [
                    ('Algebraic Data Types (enums) combined with pattern matching.', True),
                    ('Duck typing and runtime reflection.', False),
                    ('Global shared state by default.', False),
                    ('The use of \'any\' types for all interface implementations.', False),
                ]
            },
            {
                'text': 'Which comparison best describes the typical type-system philosophy of Rust versus Go?',
                'choices': [
                    ('Rust has no generics, while Go is built entirely around generics and templates.', False),
                    ('Rust emphasizes expressive modeling (e.g., algebraic data types, traits, pattern matching), while Go emphasizes simplicity with interfaces and composition.', True),
                    ('Go uses extensive pattern matching and enums as its primary modeling tools, while Rust avoids them to reduce complexity.', False),
                    ('Both languages require encoding all invariants only through comments and conventions.', False),
                ]
            },
            {
                'text': 'Which function signature is most idiomatic in Go for a function that may fail?',
                'choices': [
                    ('func f(...) throws error', False),
                    ('func f(...) (T) panicOnFailure', False),
                    ('func f(...) (T) catch(error)', False),
                    ('func f(...) (T, error)', True),
                ]
            },
            {
                'text': 'Which tools are commonly used in Go to unit test an HTTP handler without starting a real network server?',
                'choices': [
                    ('Use database/sql to simulate HTTP responses from a database.', False),
                    ('Use net/http/httptest (e.g., httptest.NewRecorder()) with http.NewRequest(...).', True),
                    ('Use runtime/pprof to validate status codes.', False),
                    ('Use os/exec to run curl and parse its output.', False),
                ]
            },
            {
                'text': 'Consider the declaration const x = 100. Which statement is true in Go?',
                'choices': [
                    ('x must include an explicit type (e.g., const x int = 100) or it will not compile.', False),
                    ('x is untyped until used, so it can be assigned to compatible numeric types (e.g., int32 or float64).', True),
                    ('x is a variable and can be reassigned later.', False),
                    ('x is always inferred as int and cannot be assigned to float64.', False),
                ]
            },
            {
                'text': 'In Go, how do "untyped" constants behave when assigned to variables of a specific type?',
                'choices': [
                    ('They have no fixed type until they are used, allowing them to be assigned to compatible types without explicit conversion.', True),
                    ('They default to interface{} type by default regardless of their literal value.', False),
                    ('They are treated as string types by default regardless of their literal value.', False),
                    ('They cause a compile-time error if the destination variable has an explicit type.', False),
                ]
            },
            {
                'text': 'What is the purpose of the errors.Unwrap function?',
                'choices': [
                    ('To retrieve the underlying error that was previously wrapped within another error.', True),
                    ('To convert an error message into a byte slice for network transmission.', False),
                    ('To reset the error state of a function so it can be called again.', False),
                    ('To delete an error from the application logs.', False),
                ]
            },
            {
                'text': 'In which scenario would Rust be a more appropriate choice than Go, based on its ability to provide predictable resource behavior?',
                'choices': [
                    ('Building a high-performance cryptography library or an embedded device driver.', True),
                    ('Developing a simple CRUD web application for a small internal team.', False),
                    ('Writing a quick script to automate cloud deployment tasks.', False),
                    ('Creating a prototype where time-to-market is the only significant constraint.', False),
                ]
            },
            {
                'text': 'When defining a method, what is the primary functional difference between using a value receiver and a pointer receiver?',
                'choices': [
                    ('A pointer receiver allows the method to modify the value to which the receiver points, while a value receiver operates on a copy.', True),
                    ('A value receiver is required for all exported methods, whereas pointer receivers are for internal use only.', False),
                    ('A pointer receiver makes the method run concurrently using goroutines by default.', False),
                    ('There is no functional difference; the choice is purely for syntax highlighting and documentation.', False),
                ]
            },
            {
                'text': 'In Go, what is the primary restriction when using the short variable declaration operator :=?',
                'choices': [
                    ('It can only be used inside functions.', True),
                    ('It can only be used for constant values.', False),
                    ('It requires explicit type annotation.', False),
                    ('It cannot be used for numeric types.', False),
                ]
            },
            {
                'text': 'What is variable shadowing in Go?',
                'choices': [
                    ('Copying a variable into another package and exporting it.', False),
                    ('Using pointers to reference the same memory from two names.', False),
                    ('Declaring a new variable in an inner scope that has the same name as a variable in an outer scope, making the outer one temporarily inaccessible.', True),
                    ('Reassigning an existing variable using the = operator.', False),
                ]
            },
            {
                'text': 'What occurs during "variable shadowing" in a Go program?',
                'choices': [
                    ('A variable in an inner scope is declared with the same name as one in an outer scope, making the outer variable temporarily inaccessible.', True),
                    ('A compiler error is triggered because the same identifier is used twice in the same package.', False),
                    ('The inner variable\'s value is automatically synchronized with the outer variable\'s value.', False),
                    ('The memory address of the outer variable is overwritten by the inner variable.', False),
                ]
            },
            {
                'text': 'When defining a variadic function in Go (e.g., func sum(nums ...int)), how is the variadic parameter treated inside the function body?',
                'choices': [
                    ('It is treated as a slice of the specified type.', True),
                    ('It is treated as a single integer representing the sum.', False),
                    ('It is treated as a pointer to the first element only.', False),
                    ('It is treated as an array of fixed size determined at compile time.', False),
                ]
            },
            {
                'text': 'Which option is a primary benefit of writing automated tests?',
                'choices': [
                    ('They automatically optimize performance without profiling.', False),
                    ('They guarantee the program will never crash in production.', False),
                    ('They remove the need for code reviews.', False),
                    ('They help catch bugs early and support safe refactoring.', True),
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

