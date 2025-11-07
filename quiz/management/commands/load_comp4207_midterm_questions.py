from django.core.management.base import BaseCommand
from quiz.models import Course, Session, Question, Choice


class Command(BaseCommand):
    help = 'Load COMP4207 Introduction to Machine Learning Midterm questions into the database'

    def handle(self, *args, **options):
        # Create or get course
        course, created = Course.objects.get_or_create(
            slug='COMP4207',
            defaults={
                'title': 'COMP4207 Introduction to Machine Learning',
                'description': 'Machine Learning course covering gradient descent, linear regression, logistic regression, neural networks, regularization, and optimization.'
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

        # All questions for COMP4207 Midterm (72 questions total)
        questions = [
            # Question 1
            {
                'text': 'How does the choice of learning rate α typically affect gradient descent?',
                'choices': [
                    ('Smaller α always leads to divergence.', False),
                    ('α has no effect on convergence behavior.', False),
                    ('Larger α always guarantees faster and stable convergence.', False),
                    ('If α is too small, progress is slow; if too large, updates may overshoot and fail to converge.', True),
                ],
                'feedback': 'If α is too small, gradient descent will converge very slowly. If α is too large, updates may overshoot the minimum and fail to converge.'
            },
            # Question 2
            {
                'text': 'Which problem is most appropriately framed as a regression task?',
                'choices': [
                    ('Deciding if a review is positive, neutral, or negative.', False),
                    ('Estimating the market price of a house from its size.', True),
                    ('Determining whether an email is spam or not.', False),
                    ('Identifying which digit (0–9) appears in an image.', False),
                ],
                'feedback': 'Estimating house price is a regression task because it predicts a continuous value. The other options are classification tasks.'
            },
            # Question 3
            {
                'text': 'In a binary classification problem (e.g., detecting cancer, y=1), what does the "Precision" metric measure?',
                'choices': [
                    ('Of all the patients who *actually* had cancer, the fraction that the model correctly identified.', False),
                    ('The harmonic mean of Precision and Recall.', False),
                    ('Of all the patients where the model predicted "cancer" (y=1), the fraction that *actually* had cancer.', True),
                    ('The total fraction of predictions (both positive and negative) that were correct.', False),
                ],
                'feedback': 'Precision = TP/(TP+FP). It measures the fraction of positive predictions that were actually correct.'
            },
            # Question 4
            {
                'text': 'What does "batch" signify in batch gradient descent?',
                'choices': [
                    ('Each update uses all training examples to compute the gradient.', True),
                    ('Each update uses a small subset of examples.', False),
                    ('It refers to processing examples in parallel across multiple machines only.', False),
                    ('Each update uses exactly one randomly chosen example.', False),
                ],
                'feedback': 'Batch gradient descent uses all training examples in each update step to compute the gradient.'
            },
            # Question 5
            {
                'text': 'When developing a machine learning model, what is the standard procedure for using the training, cross-validation (CV), and test data sets?',
                'choices': [
                    ('Train parameters on the training set, select the model hyperparameters (e.g., λ) on the CV set, and report the final generalization error on the test set.', True),
                    ('Train on the combined training and CV sets, then select the model hyperparameters using the test set.', False),
                    ('Train parameters on the training set, select hyperparameters on the test set, and report the final error on the CV set.', False),
                    ('Combine all three sets (train, CV, test) into one large set to train the model for maximum performance.', False),
                ],
                'feedback': 'The standard procedure: train on training set, tune hyperparameters on CV set, and report final results on test set.'
            },
            # Question 6
            {
                'text': 'Which statement best describes supervised learning?',
                'choices': [
                    ('The algorithm discovers structure with no targets provided.', False),
                    ('Training data provide inputs and their correct outputs (targets).', True),
                    ('It generates data without any training examples.', False),
                    ('The model interacts with an environment to maximize reward over time.', False),
                ],
                'feedback': 'Supervised learning uses labeled training data where each input has a corresponding correct output (target).'
            },
            # Question 7
            {
                'text': 'You plot a learning curve for your algorithm, showing the error as a function of the training set size (m). You observe that as m increases, both the training error (J_train) and the cross-validation error (J_cv) converge to a high error value, with J_train ≈ J_cv. What is the key takeaway from this plot?',
                'choices': [
                    ('The regularization parameter λ is too large, and decreasing it might help.', False),
                    ('The model is "just right," and no further action is needed.', False),
                    ('The model has high variance, and getting more training data is likely to help.', False),
                    ('The model has high bias, and simply getting more training data will not help solve the problem.', True),
                ],
                'feedback': 'When both errors converge to a high value with J_train ≈ J_cv, it indicates high bias (underfitting). More data won\'t help; need a more complex model.'
            },
            # Question 8
            {
                'text': 'Which formula defines the logistic sigmoid activation?',
                'choices': [
                    ('g(z) = tanh(z)', False),
                    ('g(z) = e^z / Σ_k e^z_k', False),
                    ('g(z) = 1 / (1 + e^(-z))', True),
                    ('g(z) = max(0, z)', False),
                ],
                'feedback': 'The logistic sigmoid function is g(z) = 1/(1 + e^(-z)), which maps any real number to the range (0, 1).'
            },
            # Question 9
            {
                'text': 'What typically happens if all weights in a multi-unit hidden layer are initialized to zero?',
                'choices': [
                    ('All hidden units stay identical due to symmetry and learn the same features', True),
                    ('Training becomes numerically unstable from the start', False),
                    ('The network immediately overfits', False),
                    ('Convergence always becomes faster and better', False),
                ],
                'feedback': 'Initializing all weights to zero creates symmetry - all hidden units compute the same thing and get the same gradient updates, so they never learn different features.'
            },
            # Question 10
            {
                'text': 'For univariate linear regression, which is a standard form of the hypothesis function h?',
                'choices': [
                    ('h(x) = θ₀ θ₁ x', False),
                    ('h(x) = θ₀ + θ₁ x', True),
                    ('h(x) = σ(θ₀ + θ₁ x)', False),
                    ('h(x) = θ₀ x² + θ₁', False),
                ],
                'feedback': 'For univariate linear regression, the hypothesis is h(x) = θ₀ + θ₁x, a linear function of x.'
            },
            # Question 11
            {
                'text': 'Which of the following is a method to address overfitting by keeping all features but reducing the magnitude of parameters?',
                'choices': [
                    ('Using a more complex model', False),
                    ('Regularization', True),
                    ('Increasing the number of features', False),
                    ('Manually selecting features', False),
                ],
                'feedback': 'Regularization addresses overfitting by penalizing large parameter values, effectively keeping all features but reducing their magnitude.'
            },
            # Question 12
            {
                'text': 'What is overfitting in machine learning?',
                'choices': [
                    ('A model that generalizes perfectly to all data.', False),
                    ('A model that fits the training set very well but fails to generalize to new examples.', True),
                    ('A model that ignores the training data completely.', False),
                    ('A model that performs poorly on both training and new data.', False),
                ],
                'feedback': 'Overfitting occurs when a model learns the training data too well, including noise, and fails to generalize to new examples.'
            },
            # Question 13
            {
                'text': 'In a one-vs-all classifier with 4 classes, what is the ideal one-hot target vector for class 3?',
                'choices': [
                    ('[0, 0, 1, 0]', True),
                    ('[0, 0, 0, 1]', False),
                    ('[0, 1, 0, 0]', False),
                    ('[1, 0, 0, 0]', False),
                ],
                'feedback': 'Class 3 (third position, 0-indexed as 2) should have a 1 in the third position: [0, 0, 1, 0].'
            },
            # Question 14
            {
                'text': 'Why does regularization lead to a simpler hypothesis?',
                'choices': [
                    ('By penalizing large parameter values, making the model less complex.', True),
                    ('By ignoring the training data.', False),
                    ('By increasing the number of parameters.', False),
                    ('By removing features from the model.', False),
                ],
                'feedback': 'Regularization penalizes large parameter values, which effectively reduces model complexity and leads to simpler hypotheses.'
            },
            # Question 15
            {
                'text': 'In the context of feature scaling for gradient descent, what is the specific process of mean normalization?',
                'choices': [
                    ('Calculating the Normal Equation to solve for the parameters θ analytically.', False),
                    ('Scaling the feature to ensure it is in a range of 0 ≤ x_i ≤ 1.', False),
                    ('Dividing each feature by its maximum value.', False),
                    ('Replacing the feature x_i with x_i - μ_i to give it approximately zero mean.', True),
                ],
                'feedback': 'Mean normalization replaces each feature x_i with (x_i - μ_i) to center it around zero mean.'
            },
            # Question 16
            {
                'text': 'A single sigmoid neuron with binary inputs x₁, x₂ ∈ {0,1} approximates logical AND when the parameters satisfy which condition?',
                'choices': [
                    ('Strongly positive input weights and a strongly negative bias', True),
                    ('One positive and one negative weight with zero bias', False),
                    ('All weights and bias near zero', False),
                    ('Strongly negative input weights and a strongly positive bias', False),
                ],
                'feedback': 'For AND: need both inputs to be 1. Use positive weights and negative bias so output is high only when both inputs are 1.'
            },
            # Question 17
            {
                'text': 'Why can feedforward neural networks model highly non-linear decision boundaries?',
                'choices': [
                    ('They eliminate the need for any activation functions', False),
                    ('They are strictly linear in both parameters and inputs', False),
                    ('They use hidden layers with non-linear activations that compose features', True),
                    ('They cannot represent XOR-like patterns', False),
                ],
                'feedback': 'Hidden layers with non-linear activations create complex feature compositions, enabling non-linear decision boundaries.'
            },
            # Question 18
            {
                'text': 'When building a machine learning system, such as a spam classifier, what is the primary goal of performing "error analysis"?',
                'choices': [
                    ('To manually examine the examples in the cross-validation set that the algorithm misclassified to find systematic trends and guide future development.', True),
                    ('To automatically remove the misclassified examples from the training set to improve accuracy.', False),
                    ('To calculate the F1 score, Precision, and Recall for the test set.', False),
                    ('To plot the learning curves (J_train vs. J_cv) to diagnose bias vs. variance.', False),
                ],
                'feedback': 'Error analysis involves manually examining misclassified examples to find patterns and guide improvements.'
            },
            # Question 19
            {
                'text': 'What is the primary reason for applying feature scaling in machine learning algorithms like gradient descent?',
                'choices': [
                    ('To analytically solve for the optimal parameter vector θ without iteration.', False),
                    ('To ensure that all features are on a similar scale for faster convergence of gradient descent.', True),
                    ('To increase the overall magnitude of the parameter values θ_j.', False),
                    ('To increase the number of iterations required for convergence.', False),
                ],
                'feedback': 'Feature scaling ensures features are on similar scales, which helps gradient descent converge faster by avoiding elongated error surfaces.'
            },
            # Question 20
            {
                'text': 'Why should neural-network weights be randomly initialized rather than all zeros?',
                'choices': [
                    ('Because optimizers require weights to be integers', False),
                    ('To break symmetry so hidden units learn different features', True),
                    ('To guarantee a global minimum', False),
                    ('To avoid computing gradients', False),
                ],
                'feedback': 'Random initialization breaks symmetry, allowing different hidden units to learn different features during training.'
            },
            # Question 21
            {
                'text': 'In a standard neural-network classifier for K mutually exclusive classes with one-hot targets, how many output units are typically used?',
                'choices': [
                    ('One output unit with values 1..K', False),
                    ('Two output units for any K', False),
                    ('Exactly K output units', True),
                    ('K−1 output units', False),
                ],
                'feedback': 'For K mutually exclusive classes with one-hot encoding, use K output units, one for each class.'
            },
            # Question 22
            {
                'text': 'How can logistic regression model non-linear decision boundaries?',
                'choices': [
                    ('Predict randomly for complex regions', False),
                    ('Replace the sigmoid with a linear function', False),
                    ('Use mean squared error loss', False),
                    ('Create non-linear feature mappings (e.g., polynomial features) and apply logistic regression in the expanded space', True),
                ],
                'feedback': 'Logistic regression can model non-linear boundaries by creating non-linear feature mappings (e.g., polynomial features) first.'
            },
            # Question 23
            {
                'text': 'When comparing several models on a skewed classification task, you get different Precision (P) and Recall (R) values for each. What is the F1 Score, and why is it useful?',
                'choices': [
                    ('It measures the number of True Positives minus the number of False Positives.', False),
                    ('It is another name for accuracy, but used only for skewed classes.', False),
                    ('It is the simple average of Precision and Recall ((P+R)/2), which is easier to calculate.', False),
                    ('It is the harmonic mean of Precision and Recall (2PR/(P+R)), providing a single score that balances both metrics.', True),
                ],
                'feedback': 'The F1 Score is the harmonic mean of Precision and Recall, providing a balanced measure especially useful for skewed datasets.'
            },
            # Question 24
            {
                'text': 'Which expression is the standard cost for linear regression with m examples?',
                'choices': [
                    ('J(θ) = (1/m) Σ |h(x_i) − y_i|', False),
                    ('J(θ) = Σ (h(x_i) − y_i)', False),
                    ('J(θ) = √((1/m) Σ (h(x_i) − y_i)²)', False),
                    ('J(θ) = (1/(2m)) Σ_{i=1}^m (h(x_i) − y_i)²', True),
                ],
                'feedback': 'The standard cost function for linear regression is the mean squared error: J(θ) = (1/(2m)) Σ (h(x_i) − y_i)².'
            },
            # Question 25
            {
                'text': 'Your learning algorithm performs extremely well on the training data (low J_train(θ)) but has a very high error on the cross-validation data (high J_cv(θ)). Which of the following actions is a recommended strategy to address this high variance problem?',
                'choices': [
                    ('Try decreasing the regularization parameter λ.', False),
                    ('Try adding more features or polynomial features.', False),
                    ('Use a larger neural network (more hidden layers or units).', False),
                    ('Get more training examples.', True),
                ],
                'feedback': 'High variance (overfitting) is best addressed by getting more training data, which helps the model generalize better.'
            },
            # Question 26
            {
                'text': 'In the regularization term of a neural-network cost, which parameters are typically excluded from the sum of squares?',
                'choices': [
                    ('Input features', False),
                    ('All hidden-layer weights', False),
                    ('Bias weights (the parameters connected to bias units)', True),
                    ('All output-layer weights', False),
                ],
                'feedback': 'Bias weights are typically excluded from regularization to avoid introducing bias into the model.'
            },
            # Question 27
            {
                'text': 'In linear regression, what is the primary purpose of the cost function J?',
                'choices': [
                    ('To randomly perturb parameters for exploration.', False),
                    ('To determine the number of features required.', False),
                    ('To quantify prediction error over the training set.', True),
                    ('To normalize features to zero mean and unit variance.', False),
                ],
                'feedback': 'The cost function J quantifies the prediction error over the training set, measuring how well the model fits the data.'
            },
            # Question 28
            {
                'text': 'What is the typical behavior of the cost function J(θ) during a correctly implemented gradient descent process?',
                'choices': [
                    ('The value of J(θ) should increase after every iteration.', False),
                    ('The value of J(θ) should remain constant after the first iteration.', False),
                    ('The value of J(θ) should decrease after every iteration.', True),
                    ('The value of J(θ) should fluctuate randomly.', False),
                ],
                'feedback': 'In correctly implemented gradient descent, J(θ) should decrease monotonically with each iteration until convergence.'
            },
            # Question 29
            {
                'text': 'In univariate linear regression, which update rule for θ₁ corresponds to batch gradient descent with learning rate α?',
                'choices': [
                    ('θ₁ := θ₁ − α · Σ (x_i − y_i)', False),
                    ('θ₁ := (1/m) · Σ y_i', False),
                    ('θ₁ := θ₁ − α · (1/m) · Σ_{i=1}^m (h(x_i) − y_i) x_i', True),
                    ('θ₁ := θ₁ + α · (1/m) · Σ (h(x_i) − y_i) x_i', False),
                ],
                'feedback': 'The gradient descent update for θ₁ is: θ₁ := θ₁ − α · (1/m) · Σ (h(x_i) − y_i) x_i.'
            },
            # Question 30
            {
                'text': 'The "large data" rationale suggests that having a massive training set can be more important than having the best algorithm. This approach is most likely to succeed under which of the following conditions?',
                'choices': [
                    ('Using a simple algorithm with few parameters (e.g., linear regression with few features).', False),
                    ('Using a complex algorithm with many parameters (e.g., a large neural network) AND assuming the features have sufficient information to predict y.', True),
                    ('When the features do not contain enough information to predict y (e.g., predicting price from only the number of bedrooms).', False),
                    ('When you only have a training set and no cross-validation or test set.', False),
                ],
                'feedback': 'Large data works best with complex models that can learn from it, provided the features contain sufficient information to predict y.'
            },
            # Question 31
            {
                'text': 'In standard notation, what does a₀^(j) represent in layer j?',
                'choices': [
                    ('The cost function value', False),
                    ('The output neuron index', False),
                    ('The bias unit with fixed activation 1', True),
                    ('The learning rate', False),
                ],
                'feedback': 'a₀^(j) represents the bias unit in layer j, which has a fixed activation value of 1.'
            },
            # Question 32
            {
                'text': 'After verifying with gradient checking that backpropagation is correct, what should you do before running full training?',
                'choices': [
                    ('Keep numerical gradient checking on for all iterations', False),
                    ('Turn off numerical gradient checking and train using backprop gradients', True),
                    ('Replace backprop with random gradients', False),
                    ('Set all weights to zero before each epoch', False),
                ],
                'feedback': 'Gradient checking is slow, so after verification, turn it off and train using efficient backpropagation gradients.'
            },
            # Question 33
            {
                'text': 'Why are simultaneous updates of parameters (e.g., θ₀ and θ₁) used in gradient descent implementations?',
                'choices': [
                    ('To ensure each parameter\'s update is computed from the same previous parameter values rather than partially updated ones.', True),
                    ('To randomize the order of examples within an epoch.', False),
                    ('Because it always guarantees convergence in one step.', False),
                    ('To avoid the need to choose a learning rate.', False),
                ],
                'feedback': 'Simultaneous updates ensure all parameters are updated based on the same previous values, maintaining consistency in the gradient calculation.'
            },
            # Question 34
            {
                'text': 'What is the consequence if the learning rate α for gradient descent is chosen to be too small?',
                'choices': [
                    ('The algorithm will diverge and J(θ) will increase over time.', False),
                    ('Gradient descent will converge very slowly.', True),
                    ('The Normal Equation must be used instead for convergence.', False),
                    ('The cost function J(θ) may fail to decrease on every iteration.', False),
                ],
                'feedback': 'If α is too small, gradient descent will still converge but very slowly, requiring many iterations.'
            },
            # Question 35
            {
                'text': 'You are using a logistic regression model, h_θ(x), to predict a rare and dangerous condition (e.g., cancer, y=1). You want to avoid missing cases (i.e., avoid false negatives) as much as possible. How should you adjust the classifier\'s threshold to achieve this goal?',
                'choices': [
                    ('Increase the threshold (e.g., predict y=1 if h_θ(x) ≥ 0.9), which leads to higher precision and lower recall.', False),
                    ('Lower the threshold (e.g., predict y=1 if h_θ(x) ≥ 0.3), which leads to higher recall and lower precision.', True),
                    ('Use the F1 score as the threshold.', False),
                    ('Keep the threshold at 0.5, as this always balances precision and recall.', False),
                ],
                'feedback': 'To avoid false negatives (missing cases), lower the threshold to increase recall, though this may decrease precision.'
            },
            # Question 36
            {
                'text': 'If an image has size 50×50 with three RGB channels and we use raw pixel intensities as features, how many features does one example have?',
                'choices': [
                    ('2,500', False),
                    ('1,500', False),
                    ('125,000', False),
                    ('7,500', True),
                ],
                'feedback': '50 × 50 × 3 = 7,500 features (width × height × channels).'
            },
            # Question 37
            {
                'text': 'What is the primary purpose of the Normal Equation in the context of linear regression?',
                'choices': [
                    ('To solve analytically for the parameter vector θ that minimizes the cost function.', True),
                    ('To perform feature scaling on the input data.', False),
                    ('To iteratively minimize the cost function J(θ).', False),
                    ('To define the hypothesis function h_θ(x).', False),
                ],
                'feedback': 'The Normal Equation solves analytically for θ that minimizes J(θ): θ = (X^T X)^(-1) X^T y.'
            },
            # Question 38
            {
                'text': 'In a supervised image classification task using raw pixels, what is a typical representation of one input x?',
                'choices': [
                    ('A vector of pixel intensities of the image', True),
                    ('A random noise vector unrelated to the image', False),
                    ('The class label only', False),
                    ('The network\'s learned weights', False),
                ],
                'feedback': 'In supervised image classification, input x is typically a vector containing the pixel intensities of the image.'
            },
            # Question 39
            {
                'text': 'With a sigmoid output and cross-entropy loss, what is the output-layer error term used in backpropagation?',
                'choices': [
                    ('δ^(L) = y - a^(L-1)', False),
                    ('δ^(L) = a^(L) - y', True),
                    ('δ^(L) = g\'(z^(L))', False),
                    ('δ^(L) = (Θ^(L))^T a^(L)', False),
                ],
                'feedback': 'For sigmoid output with cross-entropy loss, the output error is simply: δ^(L) = a^(L) - y.'
            },
            # Question 40
            {
                'text': 'In typical ML notation, what does the symbol m denote?',
                'choices': [
                    ('The intercept parameter.', False),
                    ('The learning rate.', False),
                    ('The number of features per example.', False),
                    ('The number of training examples.', True),
                ],
                'feedback': 'In ML notation, m typically denotes the number of training examples in the dataset.'
            },
            # Question 41
            {
                'text': 'When using an optimizer that expects a single parameter vector, how are the network weight matrices handled?',
                'choices': [
                    ('Store each matrix in a separate file', False),
                    ('Unroll all matrices into one vector and later reshape back', True),
                    ('Optimize only the last layer and fix the others', False),
                    ('Convert matrices to scalars by taking their traces', False),
                ],
                'feedback': 'Weight matrices are unrolled into a single vector for optimization, then reshaped back to matrices for forward/backward passes.'
            },
            # Question 42
            {
                'text': 'You are debugging a learning algorithm and find that its performance on the training set is poor, and its performance on the cross-validation set is similarly poor. Specifically, both J_train(θ) and J_cv(θ) are high, and J_cv(θ) ≈ J_train(θ). What is the most likely problem?',
                'choices': [
                    ('The algorithm is suffering from high variance (overfitting).', False),
                    ('The algorithm is suffering from high bias (underfitting).', True),
                    ('The regularization parameter λ is too small.', False),
                    ('The cross-validation set is too small.', False),
                ],
                'feedback': 'High training and CV errors with J_cv ≈ J_train indicates high bias (underfitting). The model is too simple.'
            },
            # Question 43
            {
                'text': 'When adding all pairwise quadratic features (including squares) x_i x_j for an input vector of length n, how does the number of such features scale with n?',
                'choices': [
                    ('O(n)', False),
                    ('O(2^n)', False),
                    ('O(log n)', False),
                    ('O(n²)', True),
                ],
                'feedback': 'Including all pairs and squares gives approximately O(n²) features: n squares + n(n-1)/2 cross-products ≈ O(n²).'
            },
            # Question 44
            {
                'text': 'In a spam classification problem, 99% of emails are non-spam (y=0) and 1% are spam (y=1). Why is "accuracy" a misleading metric in this scenario of highly skewed classes?',
                'choices': [
                    ('A simple algorithm that always predicts "non-spam" (y=0) would achieve 99% accuracy but would be useless.', True),
                    ('A high accuracy (e.g., 99%) proves the model is performing very well.', False),
                    ('Accuracy is always 50% in a binary classification problem.', False),
                    ('Accuracy cannot be computed if the classes are not balanced.', False),
                ],
                'feedback': 'With skewed classes, a trivial classifier predicting only the majority class gets high accuracy but is useless. Need precision/recall instead.'
            },
            # Question 45
            {
                'text': 'The central-difference approximation used for gradient checking of a scalar parameter θ_j is:',
                'choices': [
                    ('J(θ_j+ε) + J(θ_j-ε)', False),
                    ('(J(θ_j+ε) - J(θ_j)) / ε', False),
                    ('(J(θ_j) - J(θ_j-ε)) / ε', False),
                    ('(J(θ_j+ε) - J(θ_j-ε)) / (2ε)', True),
                ],
                'feedback': 'The central-difference approximation is: (J(θ_j+ε) - J(θ_j-ε)) / (2ε), which is more accurate than one-sided differences.'
            },
            # Question 46
            {
                'text': 'Which expression is the regularized logistic-regression cost for binary labels?',
                'choices': [
                    ('-Σ_{i=1}^m y^(i) log h_θ(x^(i))', False),
                    ('(λ/2) ||θ||₂²', False),
                    ('-(1/m)Σ_{i=1}^m [y^(i) log h_θ(x^(i)) + (1-y^(i)) log(1-h_θ(x^(i)))] + (λ/(2m))Σ_{j=1}^n θ_j²', True),
                    ('(1/m)Σ_{i=1}^m (h_θ(x^(i)) - y^(i))²', False),
                ],
                'feedback': 'Regularized logistic regression cost = logistic cost + L2 penalty term (excluding θ₀).'
            },
            # Question 47
            {
                'text': 'When performing gradient descent for multiple variables, what is the crucial aspect of updating the parameters θ_j in each iteration?',
                'choices': [
                    ('Updating only the parameters whose derivatives are non-zero.', False),
                    ('Updating only the θ₀ and θ₁ parameters.', False),
                    ('Updating the parameters sequentially from θ₀ to θ_n.', False),
                    ('Updating all parameters θ_j simultaneously using the old values of θ.', True),
                ],
                'feedback': 'All parameters must be updated simultaneously using the old parameter values to ensure consistent gradient computation.'
            },
            # Question 48
            {
                'text': 'Which of the following two-input Boolean problems is not linearly separable by a single straight line?',
                'choices': [
                    ('XOR', True),
                    ('AND', False),
                    ('OR', False),
                    ('Always-positive class vs. always-negative class', False),
                ],
                'feedback': 'XOR is not linearly separable - you cannot draw a single straight line to separate the classes. Requires non-linear decision boundary.'
            },
            # Visual Question 1
            {
                'text': 'With the standard threshold at 0.5, which condition is equivalent to predicting y = 1 for logistic regression with h_θ(x) = g(θ^T x)?',
                'choices': [
                    ('θ^T x ≥ 0', True),
                    ('θ^T x ≤ 0', False),
                    ('|θ|² ≥ 0.5', False),
                    ('h_θ(x) ≤ 0.5', False),
                ],
                'feedback': 'Predict y=1 when h_θ(x) ≥ 0.5. Since g(z) ≥ 0.5 ⟺ z ≥ 0, this means θ^T x ≥ 0.'
            },
            # Visual Question 2
            {
                'text': 'Which of the following is the sigmoid (logistic) function g(z) used in logistic regression?',
                'choices': [
                    ('g(z) = max(0, z)', False),
                    ('g(z) = tanh(z)', False),
                    ('g(z) = e^z', False),
                    ('g(z) = 1 / (1 + e^(-z))', True),
                ],
                'feedback': 'The sigmoid function is g(z) = 1/(1 + e^(-z)), which outputs values between 0 and 1.'
            },
            # Visual Question 3
            {
                'text': 'What happens if the regularization parameter λ is set to a very large value in linear regression?',
                'choices': [
                    ('Gradient descent fails to converge.', False),
                    ('The algorithm results in underfitting.', True),
                    ('The algorithm works fine without any issues.', False),
                    ('The algorithm eliminates overfitting completely.', False),
                ],
                'feedback': 'Very large λ penalizes parameters heavily, driving them close to zero, resulting in underfitting (high bias).'
            },
            # Visual Question 4
            {
                'text': 'For the logistic regression cost J(θ) = (1/m) Σ [-y^(i) log h_θ(x^(i)) - (1-y^(i)) log(1-h_θ(x^(i)))], what is the gradient component ∂J(θ)/∂θ_j?',
                'choices': [
                    ('Σ x_j^(i)', False),
                    ('(1/m) Σ (h_θ(x^(i)) - y^(i)) x_j^(i)', True),
                    ('(2/m) Σ (h_θ(x^(i)) - y^(i)) x_j^(i)', False),
                    ('(1/m) Σ (y^(i) - h_θ(x^(i))) x_j^(i)', False),
                ],
                'feedback': 'The gradient for logistic regression is: ∂J/∂θ_j = (1/m) Σ (h_θ(x^(i)) - y^(i)) x_j^(i).'
            },
            # Visual Question 5
            {
                'text': 'In multivariate linear regression with n features, what is the most concise vector representation for the hypothesis function h_θ(x)?',
                'choices': [
                    ('h_θ(x) = θ^T x', True),
                    ('θ_j := θ_j - α ∂J(θ)/∂θ_j', False),
                    ('h_θ(x) = θ₀ + θ₁ x', False),
                    ('h_θ(x) = (1/(2m)) Σ (h_θ(x^(i)) - y^(i))²', False),
                ],
                'feedback': 'In multivariate linear regression, the hypothesis is concisely written as h_θ(x) = θ^T x.'
            },
            # Visual Question 6
            {
                'text': 'Which of the following conditions can lead to the matrix X^T X being non-invertible (singular or degenerate) when using the Normal Equation?',
                'choices': [
                    ('The learning rate α is chosen to be too large.', False),
                    ('The parameter vector θ has not been initialized correctly.', False),
                    ('The cost function J(θ) is not quadratic.', False),
                    ('Having redundant features (linear dependence) or having too many features relative to the training examples (n ≥ m).', True),
                ],
                'feedback': 'X^T X is non-invertible when features are linearly dependent or when n ≥ m (more features than examples).'
            },
            # Visual Question 7
            {
                'text': 'For logistic regression with a linear model, the decision boundary (at threshold 0.5) is given by which equation?',
                'choices': [
                    ('h_θ(x) = 1', False),
                    ('θ = 0', False),
                    ('x = 0', False),
                    ('θ^T x = 0', True),
                ],
                'feedback': 'The decision boundary is where h_θ(x) = 0.5, which occurs when θ^T x = 0.'
            },
            # Visual Question 8
            {
                'text': 'In gradient descent for regularized logistic regression, how does the update differ from the unregularized version?',
                'choices': [
                    ('It includes an additional term (α λ/m)θ_j in the update for parameters j ≥ 1.', True),
                    ('It subtracts (α λ/m)θ_j from the update.', False),
                    ('It applies regularization to θ₀ as well.', False),
                    ('There is no difference in the update rule.', False),
                ],
                'feedback': 'Regularized logistic regression adds (α λ/m)θ_j term to the gradient for parameters j ≥ 1 (not θ₀).'
            },
            # Visual Question 9
            {
                'text': 'In gradient descent for regularized linear regression, how is the update for θ_j (for j ≥ 1) modified?',
                'choices': [
                    ('It adds (α λ/m) Σ θ_j to the update.', False),
                    ('It multiplies the entire update by λ.', False),
                    ('It remains the same as unregularized gradient descent.', False),
                    ('It includes a shrinkage term (1 - α λ/m)θ_j before subtracting the gradient.', True),
                ],
                'feedback': 'Regularized update: θ_j := θ_j(1 - α λ/m) - α(1/m)Σ(h_θ(x^(i)) - y^(i))x_j^(i), which shrinks θ_j.'
            },
            # Visual Question 10
            {
                'text': 'How can a model for polynomial regression, such as h_θ(x) = θ₀ + θ₁(size) + θ₂(size)² + θ₃(size)³, be implemented using the framework of multivariate linear regression?',
                'choices': [
                    ('By changing the optimization algorithm from gradient descent to the Normal Equation.', False),
                    ('By defining new features that are powers of the original feature, e.g., x₁ = size, x₂ = (size)², x₃ = (size)³.', True),
                    ('By only using the original feature without any transformation.', False),
                    ('By using a non-linear cost function instead of the mean squared error.', False),
                ],
                'feedback': 'Polynomial regression is implemented by creating new features as powers of the original feature, then applying linear regression.'
            },
            # Visual Question 11
            {
                'text': 'In the one-vs-all strategy for multi-class classification with K classes using logistic regression, how is prediction made for a new input x?',
                'choices': [
                    ('Pick argmax_{i∈{1,...,K}} h_θ^(i)(x)', True),
                    ('Average all h_θ^(i)(x) and compare to 0.5', False),
                    ('Pick the smallest index i with h_θ^(i)(x) ≥ 0.5', False),
                    ('Sum the parameter vectors and apply a single sigmoid', False),
                ],
                'feedback': 'In one-vs-all, predict the class with the highest probability: argmax_i h_θ^(i)(x).'
            },
            # Visual Question 12
            {
                'text': 'What is the cost function J(θ) used for multivariate linear regression?',
                'choices': [
                    ('θ = (X^T X)^(-1) X^T y', False),
                    ('θ_j := θ_j - α (1/m) Σ (h_θ(x^(i)) - y^(i)) x_j^(i)', False),
                    ('J(θ) = (1/(2m)) Σ (h_θ(x^(i)) - y^(i))²', True),
                    ('h_θ(x) = θ^T x', False),
                ],
                'feedback': 'The cost function for multivariate linear regression is J(θ) = (1/(2m)) Σ (h_θ(x^(i)) - y^(i))².'
            },
            # Visual Question 13
            {
                'text': 'How does regularization help when the number of features exceeds the number of examples (n > m)?',
                'choices': [
                    ('It reduces the number of features automatically.', False),
                    ('It ensures the matrix in the normal equation is invertible.', True),
                    ('It increases the number of examples.', False),
                    ('It makes the model more complex.', False),
                ],
                'feedback': 'Regularization adds λI to X^T X, making (X^T X + λI) invertible even when n > m.'
            },
            # Visual Question 14
            {
                'text': 'In regularized logistic regression, what is the cost function?',
                'choices': [
                    ('The logistic cost plus a regularization term (λ/(2m)) Σ_{j=1}^n θ_j²', True),
                    ('The regularization term only.', False),
                    ('The squared error cost with regularization.', False),
                    ('The logistic cost without any penalty.', False),
                ],
                'feedback': 'Regularized logistic regression adds the L2 penalty term (λ/(2m)) Σ θ_j² to the logistic cost.'
            },
            # Visual Question 15
            {
                'text': 'What is the normal equation for regularized linear regression?',
                'choices': [
                    ('θ = (X^T X)^(-1) X^T y without any changes.', False),
                    ('θ = (X^T X + λI)^(-1) X^T y, with I modified to not penalize θ₀.', True),
                    ('θ = X^T (X^T X + λI)^(-1) y', False),
                    ('θ = (X^T X + λ)^(-1) X^T y', False),
                ],
                'feedback': 'Regularized normal equation: θ = (X^T X + λI)^(-1) X^T y, where I has 0 at (1,1) to not penalize θ₀.'
            },
            # Visual Question 16
            {
                'text': 'Which update rule applies for batch gradient descent on logistic regression parameters θ_j with learning rate α?',
                'choices': [
                    ('θ_j := θ_j - α ∂²J(θ)/∂θ_j²', False),
                    ('θ_j := θ_j - α ∂J(θ)/∂θ_j', True),
                    ('θ_j := θ_j + α ∂J(θ)/∂θ_j', False),
                    ('θ_j := α ∂J(θ)/∂θ_j', False),
                ],
                'feedback': 'Gradient descent update: θ_j := θ_j - α ∂J(θ)/∂θ_j (move in direction opposite to gradient).'
            },
            # Visual Question 17
            {
                'text': 'In regularized linear regression, what is added to the cost function to prevent overfitting?',
                'choices': [
                    ('A term that includes θ₀ in the penalty.', False),
                    ('A term that reduces the number of features.', False),
                    ('A term that increases the learning rate.', False),
                    ('A term that penalizes large values of parameters θ_j for j = 1 to n.', True),
                ],
                'feedback': 'Regularization adds a penalty term for large parameter values: (λ/(2m)) Σ_{j=1}^n θ_j² (excluding θ₀).'
            },
            # Visual Question 18
            {
                'text': 'Suppose layer l has s_l units (excluding bias), and the next layer l+1 has s_{l+1} units. What are the dimensions of the weight matrix Θ^(l) that maps from layer l to layer l+1 (including the bias term from layer l)?',
                'choices': [
                    ('s_{l+1} × (s_l + 1)', True),
                    ('s_l × s_{l+1}', False),
                    ('s_l × (s_{l+1} + 1)', False),
                    ('(s_{l+1} + 1) × s_l', False),
                ],
                'feedback': 'Θ^(l) has dimensions s_{l+1} × (s_l + 1), where +1 accounts for the bias term from layer l.'
            },
            # Visual Question 19
            {
                'text': 'What is the logistic regression loss (cost) for a single training example (x, y) with model output h_θ(x)?',
                'choices': [
                    ('-[y log h_θ(x) + (1-y) log(1-h_θ(x))]', True),
                    ('(y - h_θ(x))²', False),
                    ('|y - h_θ(x)|', False),
                    ('-log y', False),
                ],
                'feedback': 'Logistic regression loss for one example: -[y log h_θ(x) + (1-y) log(1-h_θ(x))], the cross-entropy loss.'
            },
            # Visual Question 20
            {
                'text': 'Compared to basic gradient descent, which is a common advantage of algorithms like conjugate gradient, BFGS, or L-BFGS for fitting logistic regression?',
                'choices': [
                    ('They require fewer data points to train.', False),
                    ('They guarantee zero training error.', False),
                    ('They often converge faster and do not require manually choosing α.', True),
                    ('They avoid computing gradients entirely.', False),
                ],
                'feedback': 'Advanced optimizers like BFGS often converge faster and automatically determine the learning rate, unlike basic gradient descent.'
            },
            # Visual Question 21
            {
                'text': 'For a linear regression problem with a very large number of features n (e.g., n ≈ 10⁴), which algorithm is generally preferred, and why?',
                'choices': [
                    ('Normal Equation, because it does not require an iterative process or choosing a learning rate α.', False),
                    ('Gradient Descent, because it is less sensitive to the scale of the features than the Normal Equation.', False),
                    ('Normal Equation, because it is guaranteed to converge to the global minimum.', False),
                    ('Gradient Descent, because the computational cost of the Normal Equation, O(n³), is too slow.', True),
                ],
                'feedback': 'For large n, Normal Equation\'s O(n³) matrix inversion is too slow. Gradient descent is preferred despite being iterative.'
            },
            # Visual Question 22
            {
                'text': 'In binary classification using logistic regression, what does the model output h_θ(x) represent?',
                'choices': [
                    ('A hard label in {0, 1}.', False),
                    ('The residual y - h_θ(x).', False),
                    ('The linear score θ^T x.', False),
                    ('The estimated probability P(y = 1 | x; θ).', True),
                ],
                'feedback': 'In logistic regression, h_θ(x) represents the estimated probability that y=1 given input x.'
            },
            # Visual Question 23
            {
                'text': 'Why is mean squared error typically not used as the cost for logistic regression?',
                'choices': [
                    ('Because it requires α = 0.', False),
                    ('Because with the sigmoid, squared error makes J(θ) non-convex and can hinder convergence.', True),
                    ('Because it always overfits.', False),
                    ('Because squared error cannot be computed for binary labels.', False),
                ],
                'feedback': 'MSE with sigmoid creates a non-convex cost function with local minima. Cross-entropy is convex and preferred for logistic regression.'
            },
            # Visual Question 24
            {
                'text': 'For a hidden layer l, which expression correctly gives the backpropagated error (omitting the bias term in the next layer)?',
                'choices': [
                    ('δ^(l) = g\'(z^(l))', False),
                    ('δ^(l) = (Θ^(l))^T δ^(l+1)', False),
                    ('δ^(l) = ((Θ^(l))^T δ^(l+1))_{2:} ⊙ g\'(z^(l))', True),
                    ('δ^(l) = a^(l) - y', False),
                ],
                'feedback': 'Hidden layer error: δ^(l) = ((Θ^(l))^T δ^(l+1))_{2:} ⊙ g\'(z^(l)), where _{2:} removes bias term and ⊙ is element-wise product.'
            },
        ]

        self._load_questions(session, questions)

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] All COMP4207 Midterm questions loaded successfully!'))
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

