import re
from django.core.management.base import BaseCommand
from quiz.models import Course, Session, Question, Choice


MATH_SENTENCE_KEYWORDS = [
    " the ", " if ", " when ", " while ", " choose ", " pick ",
    " select ", " use ", " using ", " ensures ", " ensure ",
    " leads ", " causes ", " makes ", " requires ", " because ",
    " where ", " such as ", " suppose ", " includes ", " includes",
    " assumes ", " involves ", " allows ", " helps ", " defines ",
    " describes ", " which ", " whose ", " more ", " less ", " near ",
]


def should_render_as_math(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return False
    while stripped and stripped[0] in "([{" and stripped[-1] in ")]}":
        stripped = stripped[1:-1].strip()
    lower = stripped.lower()
    if any(keyword in lower for keyword in MATH_SENTENCE_KEYWORDS):
        return False
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_\\^{}()[]+-=/*.,: θδλµαβγ∑Σ√|<>≥≤'’%\"")
    if not all(ch in allowed_chars for ch in stripped):
        return False
    math_indicators = [
        "=", "\\frac", "\\sum", "∑", "Σ", "√", "_", "^", "argmax",
        "θ", "δ", "λ", "∂", "⊙"
    ]
    return any(ind in stripped for ind in math_indicators)


def wrap_math(value: str) -> str:
    return f"\\({value}\\)"


class Command(BaseCommand):
    help = 'Load 42107 Machine Learning Question Set (Midterm) into the database'

    def handle(self, *args, **options):
        course, created = Course.objects.get_or_create(
            slug='42107',
            defaults={
                'title': '42107 Machine Learning Question Set',
                'description': 'Logistic regression, gradient descent, neural networks, regularization, and evaluation metrics.'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
        else:
            self.stdout.write(f'Course already exists: {course.title}')

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

        questions = [
            {
                'text': 'Compared to basic gradient descent, which is a common advantage of algorithms like conjugate gradient, BFGS, or L-BFGS for fitting logistic regression?',
                'choices': [
                    ('They often converge faster and do not require manually choosing α', True),
                    ('They guarantee zero training error', False),
                    ('They avoid computing gradients entirely', False),
                    ('They require fewer data points to train', False),
                ],
            },
            {
                'text': 'For logistic regression with a linear model, the decision boundary (at threshold 0.5) is given by which equation?',
                'choices': [
                    ('θᵀx = 0', True),
                    ('hθ(x) = 1', False),
                    ('x = 0', False),
                    ('θ = 0', False),
                ],
            },
            {
                'text': 'What is the typical behavior of the cost function J(θ) during a correctly implemented gradient descent process?',
                'choices': [
                    ('The value of J(θ) should decrease after every iteration.', True),
                    ('The value of J(θ) should increase after every iteration.', False),
                    ('The value of J(θ) should fluctuate randomly.', False),
                    ('The value of J(θ) should remain constant after the first iteration.', False),
                ],
            },
            {
                'text': 'When performing gradient descent for multiple variables, what is the crucial aspect of updating the parameters θⱼ in each iteration?',
                'choices': [
                    ('Updating the parameters sequentially from θ₀ to θₙ.', False),
                    ('Updating all parameters θⱼ simultaneously using the old values of θ.', True),
                    ('Updating only the parameters whose derivatives are non-zero.', False),
                    ('Updating only the θ₀ and θ₁ parameters.', False),
                ],
            },
            {
                'text': 'Which update rule applies for batch gradient descent on logistic regression parameters θⱼ with learning rate α?',
                'choices': [
                    ('θⱼ := θⱼ − α ∂J(θ) / ∂θⱼ', True),
                    ('θⱼ := θⱼ + α ∂J(θ) / ∂θⱼ', False),
                    ('θⱼ := α ∂J(θ) / ∂θⱼ', False),
                    ('θⱼ := θⱼ − α ∂²J(θ) / ∂θⱼ²', False),
                ],
            },
            {
                'text': 'In univariate linear regression, which update rule for θ₁ corresponds to batch gradient descent with learning rate α?',
                'choices': [
                    ('θ₁ := θ₁ − α · (1/m) · Σᵢ (h(xᵢ) − yᵢ) xᵢ', True),
                    ('θ₁ := θ₁ + α · (1/m) · Σᵢ (h(xᵢ) − yᵢ) xᵢ', False),
                    ('θ₁ := (1/m) · Σᵢ yᵢ', False),
                    ('θ₁ := θ₁ − α · Σᵢ (xᵢ − yᵢ)', False),
                ],
            },
            {
                'text': 'For the logistic regression cost J(θ) = \\frac{1}{m} \\sum_{i=1}^{m} \\big[ -y^{(i)} \\log h_θ(x^{(i)}) - (1 - y^{(i)}) \\log (1 - h_θ(x^{(i)})) \\big], what is the gradient component ∂J(θ)/∂θⱼ ?',
                'choices': [
                    ('(\\frac{1}{m} \\sum_{i=1}^{m} (h_θ(x^{(i)}) - y^{(i)}) x^{(i)}_j)', True),
                    ('(\\frac{1}{m} \\sum_{i=1}^{m} (y^{(i)} - h_θ(x^{(i)})) x^{(i)}_j)', False),
                    ('(\\sum_{i=1}^{m} x^{(i)}_j)', False),
                    ('(\\frac{2}{m} \\sum_{i=1}^{m} (h_θ(x^{(i)}) - y^{(i)}) x^{(i)}_j)', False),
                ],
            },
            {
                'text': 'What is the consequence if the learning rate α for gradient descent is chosen to be too small?',
                'choices': [
                    ('The cost function J(θ) may fail to decrease on every iteration.', False),
                    ('Gradient descent will converge very slowly.', True),
                    ('The algorithm will diverge and J(θ) will increase over time.', False),
                    ('The Normal Equation must be used instead for convergence.', False),
                ],
            },
            {
                'text': 'In binary classification using logistic regression, what does the model output hθ(x) represent?',
                'choices': [
                    ('The estimated probability P(y = 1 | x; θ)', True),
                    ('A hard label in {0, 1}', False),
                    ('The residual y − hθ(x)', False),
                    ('The linear score θᵀx', False),
                ],
            },
            {
                'text': 'How does the choice of learning rate α typically affect gradient descent?',
                'choices': [
                    ('If α is too small, progress is slow; if too large, updates may overshoot and fail to converge.', True),
                    ('Larger α always guarantees faster and stable convergence.', False),
                    ('Smaller α always leads to divergence.', False),
                    ('α has no effect on convergence behavior.', False),
                ],
            },
            {
                'text': 'What is the logistic regression loss (cost) for a single training example (x, y) with model output hθ(x)?',
                'choices': [
                    ('-[ y \\log h_θ(x) + (1 - y) \\log(1 - h_θ(x)) ]', True),
                    ('(y − hθ(x))²', False),
                    ('|y − hθ(x)|', False),
                    ('− log y', False),
                ],
            },
            {
                'text': 'In the context of feature scaling for gradient descent, what is the specific process of mean normalization?',
                'choices': [
                    ('Dividing each feature by its maximum value.', False),
                    ('Scaling the feature to ensure it is in a range of 0 ≤ xᵢ ≤ 1.', False),
                    ('Replacing the feature xᵢ with xᵢ − μᵢ to give it approximately zero mean.', True),
                    ('Calculating the Normal Equation to solve for the parameters θ analytically.', False),
                ],
            },
            {
                'text': 'Which expression is the standard cost for linear regression with m examples?',
                'choices': [
                    ('J(θ) = \\frac{1}{2m} \\sum_{i=1}^{m} (h(x_i) - y_i)^2', True),
                    ('J(θ) = \\frac{1}{m} \\sum_{i=1}^{m} |h(x_i) - y_i|', False),
                    ('J(θ) = \\sum_{i=1}^{m} (h(x_i) - y_i)', False),
                    ('J(θ) = \\sqrt{\\frac{1}{m} \\sum_{i=1}^{m} (h(x_i) - y_i)^2}', False),
                ],
            },
            {
                'text': 'What does “batch” signify in batch gradient descent?',
                'choices': [
                    ('Each update uses all training examples to compute the gradient.', True),
                    ('Each update uses exactly one randomly chosen example.', False),
                    ('Each update uses a small subset of examples.', False),
                    ('It refers to processing examples in parallel across multiple machines only.', False),
                ],
            },
            {
                'text': 'In multivariate linear regression with n features, what is the most concise vector representation for the hypothesis function hθ(x)?',
                'choices': [
                    ('hθ(x) = θᵀx', True),
                    ('hθ(x) = θ₀ + θ₁x', False),
                    ('h_θ(x) = \\frac{1}{2m} \\sum_{i=1}^{m} (h_θ(x^{(i)}) - y^{(i)})^2', False),
                    ('θⱼ := θⱼ − α ∂J(θ)/∂θⱼ', False),
                ],
            },
            {
                'text': 'What is the cost function J(θ) used for multivariate linear regression?',
                'choices': [
                    ('J(θ) = \\frac{1}{2m} \\sum_{i=1}^m (h_θ(x^{(i)}) - y^{(i)})^2', True),
                    ('θ = (XᵀX)⁻¹ Xᵀy', False),
                    ('hθ(x) = θᵀx', False),
                    ('θⱼ := θⱼ - α \\frac{1}{m} \\sum_{i=1}^m (h_θ(x^{(i)}) - y^{(i)}) x^{(i)}_j', False),
                ],
            },
            {
                'text': 'Which of the following two-input Boolean problems is not linearly separable by a single straight line?',
                'choices': [
                    ('XOR', True),
                    ('AND', False),
                    ('OR', False),
                    ('Always-positive class vs. always-negative class', False),
                ],
            },
            {
                'text': 'If an image has size 50×50 with three RGB channels and we use raw pixel intensities as features, how many features does one example have?',
                'choices': [
                    ('7,500', True),
                    ('2,500', False),
                    ('1,500', False),
                    ('125,000', False),
                ],
            },
            {
                'text': 'When adding all pairwise quadratic features (including squares) xᵢxⱼ for an input vector of length n, how does the number of such features scale with n?',
                'choices': [
                    ('O(n²)', True),
                    ('O(n)', False),
                    ('O(log n)', False),
                    ('O(2ⁿ)', False),
                ],
            },
            {
                'text': 'Which formula defines the logistic sigmoid activation?',
                'choices': [
                    ('g(z) = \\frac{1}{1 + e^{-z}}', True),
                    ('g(z) = tanh(z)', False),
                    ('g(z) = max(0, z)', False),
                    ('g(z) = \\frac{e^z}{\\sum_k e^{z_k}}', False),
                ],
            },
            {
                'text': 'Suppose layer j has sⱼ units (excluding bias), and the next layer j+1 has sⱼ₊₁ units. What are the dimensions of the weight matrix Θ^(j) that maps from layer j to layer j+1 (including the bias term from layer j)?',
                'choices': [
                    ('sⱼ₊₁ × (sⱼ + 1)', True),
                    ('(sⱼ₊₁ + 1) × sⱼ', False),
                    ('sⱼ × sⱼ₊₁', False),
                    ('(sⱼ + 1) × (sⱼ₊₁ + 1)', False),
                ],
            },
            {
                'text': 'In a one-vs-all classifier with 4 classes, what is the ideal one-hot target vector for class 3?',
                'choices': [
                    ('0, 0, 1, 0', True),
                    ('0, 1, 0, 0', False),
                    ('1, 0, 0, 0', False),
                    ('0, 0, 0, 1', False),
                ],
            },
            {
                'text': 'In a supervised image classification task using raw pixels, what is a typical representation of one input x?',
                'choices': [
                    ('A vector of pixel intensities of the image', True),
                    ('The class label only', False),
                    ('The network’s learned weights', False),
                    ('A random noise vector unrelated to the image', False),
                ],
            },
            {
                'text': 'Why can feedforward neural networks model highly non-linear decision boundaries?',
                'choices': [
                    ('They use hidden layers with non-linear activations that compose features', True),
                    ('They are strictly linear in both parameters and inputs', False),
                    ('They eliminate the need for any activation functions', False),
                    ('They cannot represent XOR-like patterns', False),
                ],
            },
            {
                'text': 'A single sigmoid neuron with binary inputs x₁, x₂ ∈ {0,1} approximates logical AND when the parameters satisfy which condition?',
                'choices': [
                    ('Strongly positive input weights and a strongly negative bias', True),
                    ('Strongly negative input weights and a strongly positive bias', False),
                    ('All weights and bias near zero', False),
                    ('One positive and one negative weight with zero bias', False),
                ],
            },
            {
                'text': 'In standard notation, what does a₀^(j) represent in layer j?',
                'choices': [
                    ('The bias unit with fixed activation 1', True),
                    ('The learning rate', False),
                    ('The cost function value', False),
                    ('The output neuron index', False),
                ],
            },
            {
                'text': 'In a standard neural-network classifier for K mutually exclusive classes with one-hot targets, how many output units are typically used?',
                'choices': [
                    ('Exactly K output units', True),
                    ('One output unit with values 1..K', False),
                    ('Two output units for any K', False),
                    ('K−1 output units', False),
                ],
            },
            {
                'text': 'Which expression is the regularized logistic-regression cost for binary labels?',
                'choices': [
                    ('-\\frac{1}{m} \\sum_{i=1}^{m} [ y^{(i)} \\log h_θ(x^{(i)}) + (1 - y^{(i)}) \\log(1 - h_θ(x^{(i)})) ] + \\frac{λ}{2m} \\sum_{j=1}^{n} θ_j^2', True),
                    ('\\frac{1}{m} \\sum_{i=1}^m (h_θ(x^{(i)}) - y^{(i)})^2', False),
                    ('-\\sum_{i=1}^m y^{(i)} \\log h_θ(x^{(i)})', False),
                    ('\\frac{λ}{2} |θ|_2^2', False),
                ],
            },
            {
                'text': 'In the regularization term of a neural-network cost, which parameters are typically excluded from the sum of squares?',
                'choices': [
                    ('Bias weights (the parameters connected to bias units)', True),
                    ('All hidden-layer weights', False),
                    ('All output-layer weights', False),
                    ('Input features', False),
                ],
            },
            {
                'text': 'With a sigmoid output and cross-entropy loss, what is the output-layer error term used in backpropagation?',
                'choices': [
                    ('δ^(L) = a^(L) − y', True),
                    ('δ^(L) = y − a^(L−1)', False),
                    ('δ^(L) = g′(z^(L))', False),
                    ('δ^(L) = (Θ^(L))ᵀ a^(L)', False),
                ],
            },
            {
                'text': 'For a hidden layer l, which expression correctly gives the backpropagated error (omitting the bias term in the next layer)?',
                'choices': [
                    ('δ^(l) = ((Θ^(l))ᵀ δ^(l+1))₂: ∘ g′(z^(l))', True),
                    ('δ^(l) = (Θ^(l))ᵀ δ^(l+1)', False),
                    ('δ^(l) = a^(l) − y', False),
                    ('δ^(l) = g(z^(l))', False),
                ],
            },
            {
                'text': 'The central-difference approximation used for gradient checking of a scalar parameter θⱼ is:',
                'choices': [
                    ('(\\frac{J(θ_j + ε) - J(θ_j - ε)}{2ε})', True),
                    ('(\\frac{J(θ_j + ε) - J(θ_j)}{ε})', False),
                    ('(\\frac{J(θ_j) - J(θ_j - ε)}{ε})', False),
                    ('(J(θ_j + ε) + J(θ_j - ε))', False),
                ],
            },
            {
                'text': 'Why should neural-network weights be randomly initialized rather than all zeros?',
                'choices': [
                    ('To break symmetry so hidden units learn different features', True),
                    ('To guarantee a global minimum', False),
                    ('To avoid computing gradients', False),
                    ('Because optimizers require weights to be integers', False),
                ],
            },
            {
                'text': 'What typically happens if all weights in a multi-unit hidden layer are initialized to zero?',
                'choices': [
                    ('All hidden units stay identical due to symmetry and learn the same features', True),
                    ('The network immediately overfits', False),
                    ('Training becomes numerically unstable from the start', False),
                    ('Convergence always becomes faster and better', False),
                ],
            },
            {
                'text': 'When using an optimizer that expects a single parameter vector, how are the network weight matrices handled?',
                'choices': [
                    ('Unroll all matrices into one vector and later reshape back', True),
                    ('Store each matrix in a separate file', False),
                    ('Optimize only the last layer and fix the others', False),
                    ('Convert matrices to scalars by taking their traces', False),
                ],
            },
            {
                'text': 'After verifying with gradient checking that backpropagation is correct, what should you do before running full training?',
                'choices': [
                    ('Turn off numerical gradient checking and train using backprop gradients', True),
                    ('Keep numerical gradient checking on for all iterations', False),
                    ('Replace backprop with random gradients', False),
                    ('Set all weights to zero before each epoch', False),
                ],
            },
            {
                'text': 'Which of the following conditions can lead to the matrix XᵀX being non-invertible (singular or degenerate) when using the Normal Equation?',
                'choices': [
                    ('Having redundant features (linear dependence) or having too many features relative to the training examples (n ≥ m).', True),
                    ('The learning rate α is chosen to be too large.', False),
                    ('The cost function J(θ) is not quadratic.', False),
                    ('The parameter vector θ has not been initialized correctly.', False),
                ],
            },
            {
                'text': 'How can logistic regression model non-linear decision boundaries?',
                'choices': [
                    ('Create non-linear feature mappings (e.g., polynomial features) and apply logistic regression in the expanded space', True),
                    ('Replace the sigmoid with a linear function', False),
                    ('Use mean squared error loss', False),
                    ('Predict randomly for complex regions', False),
                ],
            },
            {
                'text': 'What is the primary purpose of the Normal Equation in the context of linear regression?',
                'choices': [
                    ('To solve analytically for the parameter vector θ that minimizes the cost function.', True),
                    ('To iteratively minimize the cost function J(θ).', False),
                    ('To define the hypothesis function hθ(x).', False),
                    ('To perform feature scaling on the input data.', False),
                ],
            },
            {
                'text': 'For a linear regression problem with a very large number of features n (e.g., n ≈ 10⁶), which algorithm is generally preferred, and why?',
                'choices': [
                    ('Gradient Descent, because the computational cost of the Normal Equation, O(n³), is too slow.', True),
                    ('Normal Equation, because it does not require an iterative process or choosing a learning rate α.', False),
                    ('Normal Equation, because it is guaranteed to converge to the global minimum.', False),
                    ('Gradient Descent, because it is less sensitive to the scale of the features than the Normal Equation.', False),
                ],
            },
            {
                'text': 'In typical ML notation, what does the symbol m denote?',
                'choices': [
                    ('The number of training examples.', True),
                    ('The number of features per example.', False),
                    ('The learning rate.', False),
                    ('The intercept parameter.', False),
                ],
            },
            {
                'text': 'In the one-vs-all strategy for multi-class classification with K classes using logistic regression, how is prediction made for a new input x?',
                'choices': [
                    ('Pick (argmax_{i∈{1,...,K}} h^{(i)}_θ(x))', True),
                    ('Average all (h^{(i)}_θ(x)) and compare to 0.5', False),
                    ('Pick the smallest index i with (h^{(i)}_θ(x) ≥ 0.5)', False),
                    ('Sum the parameter vectors and apply a single sigmoid', False),
                ],
            },
            {
                'text': 'How can a model for polynomial regression, such as h_θ(x) = θ_0 + θ_1 (size) + θ_2 (size)^2 + θ_3 (size)^3, be implemented using the framework of multivariate linear regression?',
                'choices': [
                    ('By defining new features that are powers of the original feature, e.g., x₁ = size, x₂ = (size)², x₃ = (size)³.', True),
                    ('By changing the optimization algorithm from gradient descent to the Normal Equation.', False),
                    ('By using a non-linear cost function instead of the mean squared error.', False),
                    ('By only using the original feature without any transformation.', False),
                ],
            },
            {
                'text': 'What is the primary reason for applying feature scaling in machine learning algorithms like gradient descent?',
                'choices': [
                    ('To ensure that all features are on a similar scale for faster convergence of gradient descent.', True),
                    ('To increase the number of iterations required for convergence.', False),
                    ('To analytically solve for the optimal parameter vector θ without iteration.', False),
                    ('To increase the overall magnitude of the parameter values θⱼ.', False),
                ],
            },
            {
                'text': 'In linear regression, what is the primary purpose of the cost function J?',
                'choices': [
                    ('To quantify prediction error over the training set.', True),
                    ('To randomly perturb parameters for exploration.', False),
                    ('To normalize features to zero mean and unit variance.', False),
                    ('To determine the number of features required.', False),
                ],
            },
            {
                'text': 'What is overfitting in machine learning?',
                'choices': [
                    ('A model that fits the training set very well but fails to generalize to new examples.', True),
                    ('A model that performs poorly on both training and new data.', False),
                    ('A model that ignores the training data completely.', False),
                    ('A model that generalizes perfectly to all data.', False),
                ],
            },
            {
                'text': 'In gradient descent for regularized logistic regression, how does the update differ from the unregularized version?',
                'choices': [
                    ('It includes an additional term (αλ/m) θⱼ in the update for parameters j ≥ 1.', True),
                    ('It subtracts (αλ/m) θⱼ from the update.', False),
                    ('It applies regularization to θ₀ as well.', False),
                    ('There is no difference in the update rule.', False),
                ],
            },
            {
                'text': 'Which of the following is a method to address overfitting by keeping all features but reducing the magnitude of parameters?',
                'choices': [
                    ('Regularization', True),
                    ('Manually selecting features', False),
                    ('Increasing the number of features', False),
                    ('Using a more complex model', False),
                ],
            },
            {
                'text': 'In regularized linear regression, what is added to the cost function to prevent overfitting?',
                'choices': [
                    ('A term that penalizes large values of parameters θⱼ for j = 1 to n.', True),
                    ('A term that includes θ₀ in the penalty.', False),
                    ('A term that reduces the number of features.', False),
                    ('A term that increases the learning rate.', False),
                ],
            },
            {
                'text': 'What happens if the regularization parameter λ is set to a very large value in linear regression?',
                'choices': [
                    ('The algorithm results in underfitting.', True),
                    ('The algorithm eliminates overfitting completely.', False),
                    ('Gradient descent fails to converge.', False),
                    ('The algorithm works fine without any issues.', False),
                ],
            },
            {
                'text': 'In gradient descent for regularized linear regression, how is the update for θⱼ (for j ≥ 1) modified?',
                'choices': [
                    ('It includes a shrinkage term (1 − αλ/m) θⱼ before subtracting the gradient.', True),
                    ('It adds (αλ/m) Σ θⱼ to the update.', False),
                    ('It remains the same as unregularized gradient descent.', False),
                    ('It multiplies the entire update by λ.', False),
                ],
            },
            {
                'text': 'What is the normal equation for regularized linear regression?',
                'choices': [
                    ('θ = (XᵀX + λI)⁻¹ Xᵀy, with I modified to not penalize θ₀.', True),
                    ('θ = (XᵀX)⁻¹ Xᵀy without any changes.', False),
                    ('θ = Xᵀ (XXᵀ + λI)⁻¹ y.', False),
                    ('θ = (XᵀX + λ)⁻¹ Xᵀy.', False),
                ],
            },
            {
                'text': 'How does regularization help when the number of features exceeds the number of examples (n > m)?',
                'choices': [
                    ('It ensures the matrix in the normal equation is invertible.', True),
                    ('It reduces the number of features automatically.', False),
                    ('It increases the number of examples.', False),
                    ('It makes the model more complex.', False),
                ],
            },
            {
                'text': 'In regularized logistic regression, what is the cost function?',
                'choices': [
                    ('The logistic cost plus a regularization term ( \\frac{λ}{2m} \\sum_{j=1}^{n} θ_j^2 ).', True),
                    ('The squared error cost with regularization.', False),
                    ('The logistic cost without any penalty.', False),
                    ('The regularization term only.', False),
                ],
            },
            {
                'text': 'Why does regularization lead to a simpler hypothesis?',
                'choices': [
                    ('By penalizing large parameter values, making the model less complex.', True),
                    ('By removing features from the model.', False),
                    ('By increasing the number of parameters.', False),
                    ('By ignoring the training data.', False),
                ],
            },
            {
                'text': 'Which problem is most appropriately framed as a regression task?',
                'choices': [
                    ('Estimating the market price of a house from its size.', True),
                    ('Determining whether an email is spam or not.', False),
                    ('Identifying which digit (0–9) appears in an image.', False),
                    ('Deciding if a review is positive, neutral, or negative.', False),
                ],
            },
            {
                'text': 'Which of the following is the sigmoid (logistic) function g(z) used in logistic regression?',
                'choices': [
                    ('g(z) = \\frac{1}{1 + e^{-z}}', True),
                    ('g(z) = e^z', False),
                    ('g(z) = max(0, z)', False),
                    ('g(z) = tanh(z)', False),
                ],
            },
            {
                'text': 'Why are simultaneous updates of parameters (e.g., θ₀ and θ₁) used in gradient descent implementations?',
                'choices': [
                    ('To ensure each parameter’s update is computed from the same previous parameter values rather than partially updated ones.', True),
                    ('To randomize the order of examples within an epoch.', False),
                    ('To avoid the need to choose a learning rate.', False),
                    ('Because it always guarantees convergence in one step.', False),
                ],
            },
            {
                'text': 'Which statement best describes supervised learning?',
                'choices': [
                    ('Training data provide inputs and their correct outputs (targets).', True),
                    ('The algorithm discovers structure with no targets provided.', False),
                    ('The model interacts with an environment to maximize reward over time.', False),
                    ('It generates data without any training examples.', False),
                ],
            },
            {
                'text': 'With the standard threshold at 0.5, which condition is equivalent to predicting y = 1 for logistic regression with hθ(x) = g(θᵀx)?',
                'choices': [
                    ('θᵀx ≥ 0', True),
                    ('θᵀx ≤ 0', False),
                    ('hθ(x) ≤ 0.5', False),
                    ('∥θ∥₂ ≥ 0.5', False),
                ],
            },
            {
                'text': 'For univariate linear regression, which is a standard form of the hypothesis function h?',
                'choices': [
                    ('h(x) = θ₀ + θ₁ x', True),
                    ('h(x) = θ₀ x² + θ₁', False),
                    ('h(x) = σ(θ₀ + θ₁ x)', False),
                    ('h(x) = θ₀ θ₁ x', False),
                ],
            },
            {
                'text': 'Why is mean squared error typically not used as the cost for logistic regression?',
                'choices': [
                    ('Because with the sigmoid, squared error makes J(θ) non-convex and can hinder convergence', True),
                    ('Because squared error cannot be computed for binary labels', False),
                    ('Because it always overfits', False),
                    ('Because it requires α = 0', False),
                ],
            },
            {
                'text': 'In a binary classification problem (e.g., detecting cancer, y = 1), what does the "Precision" metric measure?',
                'choices': [
                    ('Of all the patients where the model predicted "cancer" (y = 1), the fraction that actually had cancer.', True),
                    ('Of all the patients who actually had cancer, the fraction that the model correctly identified.', False),
                    ('The total fraction of predictions (both positive and negative) that were correct.', False),
                    ('The harmonic mean of Precision and Recall.', False),
                ],
            },
            {
                'text': 'When building a machine learning system, such as a spam classifier, what is the primary goal of performing "error analysis"?',
                'choices': [
                    ('To manually examine the examples in the cross-validation set that the algorithm misclassified to find systematic trends and guide future development.', True),
                    ('To plot the learning curves (J_train vs. J_cv) to diagnose bias vs. variance.', False),
                    ('To automatically remove the misclassified examples from the training set to improve accuracy.', False),
                    ('To calculate the F1 score, Precision, and Recall for the test set.', False),
                ],
            },
            {
                'text': 'When comparing several models on a skewed classification task, you get different Precision (P) and Recall (R) values for each. What is the F1 Score, and why is it useful?',
                'choices': [
                    ('It is the harmonic mean of Precision and Recall ( \\left( \\frac{2PR}{P+R} \\right) ), providing a single score that balances both metrics.', True),
                    ('It is the simple average of Precision and Recall ( \\frac{P+R}{2} ), which is easier to calculate.', False),
                    ('It is another name for accuracy, but used only for skewed classes.', False),
                    ('It measures the number of True Positives minus the number of False Positives.', False),
                ],
            },
            {
                'text': 'The "large data" rationale suggests that having a massive training set can be more important than having the best algorithm. This approach is most likely to succeed under which of the following conditions?',
                'choices': [
                    ('Using a complex algorithm with many parameters (e.g., a large neural network) AND assuming the features have sufficient information to predict y.', True),
                    ('Using a simple algorithm with few parameters (e.g., linear regression with few features).', False),
                    ('When you only have a training set and no cross-validation or test set.', False),
                    ('When the features do not contain enough information to predict y (e.g., predicting price from only the number of bedrooms).', False),
                ],
            },
            {
                'text': 'You are using a logistic regression model hθ(x) to predict a rare and dangerous condition (e.g., cancer, y = 1). You want to avoid missing cases (i.e., avoid false negatives) as much as possible. How should you adjust the classifier’s threshold to achieve this goal?',
                'choices': [
                    ('Lower the threshold (e.g., predict y = 1 if hθ(x) ≥ 0.3), which leads to higher recall and lower precision.', True),
                    ('Increase the threshold (e.g., predict y = 1 if hθ(x) ≥ 0.9), which leads to higher precision and lower recall.', False),
                    ('Keep the threshold at 0.5, as this always balances precision and recall.', False),
                    ('Use the F1 score as the threshold.', False),
                ],
            },
            {
                'text': 'In a spam classification problem, 99% of emails are non-spam (y = 0). Which of the following is true?',
                'choices': [
                    ('A simple algorithm that always predicts "non-spam" (y = 0) would achieve 99% accuracy.', True),
                    ('Accuracy is always 50%.', False),
                    ('Accuracy cannot be computed if the classes are not balanced.', False),
                    ('A high accuracy (e.g., 99%) necessarily implies a good classifier.', False),
                ],
            },
            {
                'text': 'When developing a machine learning model, what is the standard procedure for using the training, cross-validation (CV), and test data sets?',
                'choices': [
                    ('Train parameters on the training set, select the model hyperparameters (e.g., λ) on the CV set, and report the final generalization error on the test set.', True),
                    ('Train parameters on the training set, select hyperparameters on the test set, and report the final error on the CV set.', False),
                    ('Train on the combined training and CV sets, then select the model hyperparameters using the test set.', False),
                    ('Combine all three sets (train, CV, test) into one large set to train the model for maximum performance.', False),
                ],
            },
            {
                'text': 'You are debugging a learning algorithm and find that its performance on the training set is poor, and its performance on the cross-validation set is similarly poor. Specifically, both J_train(θ) and J_cv(θ) are high, and J_cv(θ) ≈ J_train(θ). What is the most likely problem?',
                'choices': [
                    ('The algorithm is suffering from high bias (underfitting).', True),
                    ('The algorithm is suffering from high variance (overfitting).', False),
                    ('The regularization parameter λ is too small.', False),
                    ('The cross-validation set is too small.', False),
                ],
            },
            {
                'text': 'Your learning algorithm performs extremely well on the training data (low J_train(θ)) but has a very high error on the cross-validation data (high J_cv(θ)). Which of the following actions is a recommended strategy to address this high variance problem?',
                'choices': [
                    ('Get more training examples.', True),
                    ('Try adding more features or polynomial features.', False),
                    ('Try decreasing the regularization parameter λ.', False),
                    ('Use a larger neural network (more hidden layers or units).', False),
                ],
            },
            {
                'text': 'You plot a learning curve for your algorithm, showing the error as a function of the training set size (m). You observe that as m increases, both the training error (J_train) and the cross-validation error (J_cv) converge to a high error value, with J_train ≈ J_cv. What is the key takeaway from this plot?',
                'choices': [
                    ('The model has high bias, and simply getting more training data will not help solve the problem.', True),
                    ('The model has high variance, and getting more training data is likely to help.', False),
                    ('The model is "just right," and no further action is needed.', False),
                    ('The regularization parameter λ is too large, and decreasing it might help.', False),
                ],
            },
        ]

        self._load_questions(session, questions)

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] All 42107 Midterm questions loaded successfully!'))
        self.stdout.write(f'Total questions in Midterm: {session.questions.count()}')

    def _load_questions(self, session, questions_data):
        existing_count = session.questions.count()
        created_count = 0
        updated_count = 0

        for idx, q_data in enumerate(questions_data, start=1):
            original_text = q_data['text']
            text = original_text

            def replace_bracket_math(match):
                inner = match.group(1).strip()
                if should_render_as_math(inner):
                    return f"[{wrap_math(inner)}]"
                return match.group(0)

            text = re.sub(r"\[(.*?)\]", replace_bracket_math, text, flags=re.S)

            processed_choices = []
            for choice_text, is_correct in q_data['choices']:
                c_text = wrap_math(choice_text) if should_render_as_math(choice_text) else choice_text
                processed_choices.append((c_text, is_correct))

            question = Question.objects.filter(session=session, text=original_text).first()
            if not question and original_text != text:
                question = Question.objects.filter(session=session, text=text).first()

            if question:
                question.order = idx
                question.is_active = True
                question.text = text
                question.save(update_fields=['order', 'is_active', 'text'])

                existing_choices = list(question.choices.all())
                if len(existing_choices) == len(processed_choices):
                    for choice, (choice_text, is_correct) in zip(existing_choices, processed_choices):
                        choice.text = choice_text
                        choice.is_correct = is_correct
                        choice.save(update_fields=['text', 'is_correct'])
                else:
                    question.choices.all().delete()
                    for choice_text, is_correct in processed_choices:
                        Choice.objects.create(
                            question=question,
                            text=choice_text,
                            is_correct=is_correct
                        )

                updated_count += 1
                self.stdout.write(f'  [~] Updated question {idx}')
            else:
                question = Question.objects.create(
                    session=session,
                    text=text,
                    order=idx,
                    is_active=True
                )

                for choice_text, is_correct in processed_choices:
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=is_correct
                    )
                created_count += 1
                self.stdout.write(f'  [+] Created question {idx}')

        self.stdout.write(f'\nSummary: Created {created_count} questions, updated {updated_count} questions.')

