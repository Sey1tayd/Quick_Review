from django.core.management.base import BaseCommand
from django.db.models import Max
from quiz.models import Course, Session, Question, Choice
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Adds questions for COMP4207'

    def handle(self, *args, **options):
        # Create or get course
        course, created = Course.objects.get_or_create(
            slug='comp4207',
            defaults={'title': 'COMP4207'}
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
                'text': 'In a density-estimation approach to anomaly detection, a new examplexis typically flagged as anomalous when:',
                'choices': [
                    ('p(x)<ϵfor a chosen thresholdϵ.', True),
                    ('p(x)>ϵfor a chosen thresholdϵ.', False),
                    ('The model predicts the most likely class label forxusing a softmax layer.', False),
                    ('‖x‖is maximized compared to all training points.', False),
                ]
            },
            {
                'text': 'Which situation most strongly motivates using anomaly detection rather than standard supervised classification?',
                'choices': [
                    ('There are very few labeled anomalies, and future anomalies may look different from those seen before.', True),
                    ('There are many labeled anomalies and they are all highly similar to each other.', False),
                    ('All classes are balanced, and you want to minimize mean squared error.', False),
                    ('You have a deterministic rule that exactly separates normal and anomalous data.', False),
                ]
            },
            {
                'text': 'For a univariate Gaussian (normal) distribution, which pair of parameters fully specifies the distribution?',
                'choices': [
                    ('Meanμand varianceσ2.', True),
                    ('Median and interquartile range.', False),
                    ('Skewness and kurtosis.', False),
                    ('Minimum and maximum values.', False),
                ]
            },
            {
                'text': 'Given training values{x(1),…,x(m)}, which formulas are commonly used to estimate Gaussian parameters for anomaly detection?',
                'choices': [
                    ('μ=1m∑i=1mx(i)andσ2=1m∑i=1m(x(i)−μ)2.', True),
                    ('μ=∑i=1mx(i)andσ2=∑i=1m(x(i)−μ)2(no averaging).', False),
                    ('μ=maxix(i)andσ2=minix(i).', False),
                    ('μ=0andσ2=1for all features by default.', False),
                ]
            },
            {
                'text': 'In a common anomaly detection baseline,p(x)is computed as a product of per-feature densitiesp(xj). What is the key modeling assumption behind this approach?',
                'choices': [
                    ('The featuresx1,…,xnare conditionally independent under the modeled distribution.', True),
                    ('All features must be binary-valued.', False),
                    ('The thresholdϵis always equal to0.5.', False),
                    ('Every feature must have exactly the same mean and variance.', False),
                ]
            },
            {
                'text': 'In practice, why is a cross-validation (CV) set containing some labeled anomalies often used when building an anomaly detection system?',
                'choices': [
                    ('To tune choices such as the thresholdϵand evaluate performance with metrics like precision/recall orF1.', True),
                    ('To ensure the training set contains as many anomalies as possible.', False),
                    ('To replace the need for a test set entirely.', False),
                    ('To make the Gaussian distribution symmetric.', False),
                ]
            },
            {
                'text': 'If an example is truly anomalous and the system flags it as anomalous, this outcome is called:',
                'choices': [
                    ('True positive.', True),
                    ('False positive.', False),
                    ('False negative.', False),
                    ('True negative.', False),
                ]
            },
            {
                'text': 'When a feature has a strongly skewed, non-Gaussian distribution, which technique is commonly used to make it closer to Gaussian for modeling?',
                'choices': [
                    ('Apply a monotonic transform such aslog\u2061(x)orlog\u2061(x+1).', True),
                    ('Randomly permute the feature values across examples.', False),
                    ("Replace every value with the feature's maximum.", False),
                    ('Convert the feature into a one-hot vector with one category per sample.', False),
                ]
            },
            {
                'text': 'Compared to modeling each feature separately, what is a major advantage of using a multivariate Gaussian model for anomaly detection?',
                'choices': [
                    ('It can capture correlations between features via the covariance matrixΣ.', True),
                    ('It guarantees perfect separation of normal and anomalous examples.', False),
                    ('It eliminates the need to estimate any parameters from data.', False),
                    ('It only works when all features are independent.', False),
                ]
            },
            {
                'text': 'A common failure mode in anomaly detection is whenp(x)is similarly large for both normal and anomalous examples. Which response is most appropriate?',
                'choices': [
                    ('Create more informative features (including ones capturing unusual combinations) and/or switch to a model that captures correlations.', True),
                    ('Setϵ=1so that all examples are flagged as anomalies.', False),
                    ('Remove the CV set and chooseϵrandomly.', False),
                    ('Stop using probabilities and classify anomalies by sorting examples alphabetically by ID.', False),
                ]
            },
            {
                'text': 'Which fairness criterion requires that the True Positive Rate (TPR) and False Positive Rate (FPR) be equal across different protected groups?',
                'choices': [
                    ('Demographic parity [cite: 1219]', False),
                    ('Equalized odds [cite: 1220]', True),
                    ('Predictive parity [cite: 1221]', False),
                    ('K-anonymity [cite: 1264]', False),
                ]
            },
            {
                'text': 'Which of the following is a common application of anomaly detection?',
                'choices': [
                    ('Fraud detection in user activities', True),
                    ('Image classification for object recognition', False),
                    ('Sentiment analysis in text data', False),
                    ('Time series forecasting for stock prices', False),
                ]
            },
            {
                'text': 'What is the primary goal of anomaly detection in machine learning?',
                'choices': [
                    ('To identify unusual patterns or outliers in data that do not conform to expected behavior', True),
                    ('To classify data into predefined categories', False),
                    ('To predict continuous values based on input features', False),
                    ('To cluster similar data points together', False),
                ]
            },
            {
                'text': 'In which of the following scenarios is an Anomaly Detection algorithm generally preferred over a standard Supervised Learning approach?',
                'choices': [
                    ("When there is a very small number of positive examples(y=1)and many different 'types' of anomalies that may look different in the future.", True),
                    ('When there are a large number of both positive and negative examples in the training set.', False),
                    ('When the future positive examples are expected to be very similar to the ones currently in the training set.', False),
                    ('When the goal is to perform weather prediction or email spam classification with high-volume labeled data.', False),
                ]
            },
            {
                'text': 'What is a key difference between anomaly detection and supervised learning?',
                'choices': [
                    ('Anomaly detection typically has very few positive examples and many types of anomalies', True),
                    ('Supervised learning has few positive examples while anomaly detection has many', False),
                    ('Anomaly detection requires labeled data for all examples', False),
                    ('Supervised learning is used for unsupervised problems', False),
                ]
            },
            {
                'text': 'In the context of very large datasets (e.g.,m=300,000,000), why is Batch Gradient Descent typically inefficient?',
                'choices': [
                    ('It requires a higher learning rateαwhich leads to divergence.', False),
                    ('It can only be used for linear regression models.', False),
                    ('It must process and sum over every single training example before making a single parameter update.', True),
                    ('It is mathematically impossible to compute the derivative for largem.', False),
                ]
            },
            {
                'text': 'What is a key characteristic of collaborative filtering in recommender systems?',
                'choices': [
                    ('It learns both user parameters and item features simultaneously from ratings data', True),
                    ('It relies solely on predefined item features', False),
                    ('It uses only user demographics for predictions', False),
                    ('It ignores missing ratings in the dataset', False),
                ]
            },
            {
                'text': 'When starting the optimization for a collaborative filtering algorithm, how should the featuresxand parametersθbe initialized?',
                'choices': [
                    ('To small random values to ensure symmetry breaking.', True),
                    ('To all zeros to speed up the calculation of the gradient.', False),
                    ('To very large values to ensure the algorithm finds the global maximum.', False),
                    ('To the exact mean of the existing ratings in the matrix.', False),
                ]
            },
            {
                'text': 'What is the joint optimization objective in collaborative filtering?',
                'choices': [
                    ('12∑(i,j):r(i,j)=1((θ(j))Tx(i)−y(i,j))2+λ2∑i=1nm∑k=1n(xk(i))2+λ2∑j=1nu∑k=1n(θk(j))2', True),
                    ('∑(i,j):r(i,j)=1((θ(j))Tx(i)+y(i,j))2+λ∑i=1nm∑k=1n(xk(i))2', False),
                    ('12∑(i,j):r(i,j)=0((θ(j))Tx(i)−y(i,j))2', False),
                    ('λ∑j=1nu∑k=1n(θk(j))2−∑(i,j):r(i,j)=1((θ(j))Tx(i))', False),
                ]
            },
            {
                'text': 'What is a primary characteristic of Collaborative Filtering compared to Content-Based recommendation?',
                'choices': [
                    ('It can learn its own features for items instead of relying on pre-defined features.', True),
                    ("It requires a detailed manual description of every movie's genre.", False),
                    ('It only works if the user has provided a biography of their interests.', False),
                    ('It is used exclusively for predicting star ratings and not for finding similar items.', False),
                ]
            },
            {
                'text': 'In a content-based recommender system, given a feature vector for a moviex(i)and a parameter vector for a userθ(j), how is the rating predicted?',
                'choices': [
                    ('Using the inner product(θ(j))Tx(i).', True),
                    ('Using the Euclidean distance||θ(j)−x(i)||.', False),
                    ('By calculating the mean of all ratings in the matrixY.', False),
                    ('Using the product of the sums∑θ(j)×∑x(i).', False),
                ]
            },
            {
                'text': 'In content-based recommender systems, how is the predicted rating for a userjand movieicalculated?',
                'choices': [
                    ('(θ(j))Tx(i)', True),
                    ('∑k=1nθk(j)+xk(i)', False),
                    ('‖θ(j)−x(i)‖', False),
                    ('∏k=1nθk(j)⋅xk(i)', False),
                ]
            },
            {
                'text': 'In the basic operation principle of Reinforcement Learning, what is the primary role of theAgent?',
                'choices': [
                    ('To interpret the state and provide labels for supervised learning.', False),
                    ('To pick an action based on observations and rewards in order to maximize long-term return.', True),
                    ('To define the constant time intervalΔtfor the environment.', False),
                    ('To emit subsequent statesxk+1to the interpreter.', False),
                ]
            },
            {
                'text': 'In a Multivariate Gaussian model, what is a necessary condition for the covariance matrixΣto be invertible?',
                'choices': [
                    ('The number of training examplesmmust be greater than the number of featuresn.', True),
                    ('The thresholdϵmust be set to zero.', False),
                    ('All features must be perfectly correlated with one another.', False),
                    ('The mean vectorμmust consist only of positive values.', False),
                ]
            },
            {
                'text': 'Which data splitting strategy is most effective at preventing temporal leakage when evaluating models for forecasting or time-series tasks?',
                'choices': [
                    ('IID random splitting [cite: 933]', False),
                    ('Time-based splitting [cite: 934]', True),
                    ('K-fold cross-validation [cite: 940]', False),
                    ('Grouped splitting [cite: 935]', False),
                ]
            },
            {
                'text': 'When implementing Map-Reduce logic on a single machine with multiple CPU cores, how is the training set typically handled?',
                'choices': [
                    ('Each core runs the entire dataset sequentially.', False),
                    ('The training set is split into subsets, and each core computes a partial sum for its respective subset.', True),
                    ("One core handles all the math while the others wait for the 'Reduce' step.", False),
                    ('The cores use a shared memory to process the same single example simultaneously.', False),
                ]
            },
            {
                'text': 'When developing an anomaly detection system, what is the typical recommendation for the composition of the Training set?',
                'choices': [
                    ('It should consist only of examples assumed to be normal (non-anomalous).', True),
                    ('It should consist of 50% normal examples and 50% anomalous examples.', False),
                    ('It should consist only of anomalous examples.', False),
                    ('It should be empty, as the model is purely unsupervised.', False),
                ]
            },
            {
                'text': 'How isConcept Driftdefined in the context of model monitoring?',
                'choices': [
                    ('A change in the relationship between inputs and targets, represented asp(y|x)[cite: 1105, 1126]', True),
                    ('A shift in the distribution of input features, represented asp(x)[cite: 1104, 1121]', False),
                    ('The presence of missing values in the production data store [cite: 1060]', False),
                    ('A failure to meet Service Level Objectives (SLOs) [cite: 1031]', False),
                ]
            },
            {
                'text': 'In the context of density estimation for anomaly detection, given a modelp(x)and a thresholdϵ, when is a test examplextestflagged as an anomaly?',
                'choices': [
                    ('Ifp(xtest)<ϵ', True),
                    ('Ifp(xtest)≥ϵ', False),
                    ('Ifp(xtest)=1', False),
                    ('If the varianceσ2is greater thanϵ', False),
                ]
            },
            {
                'text': 'InContinuing Tasks, which do not have a natural end, how is the returngktypically calculated to ensure the sum remains finite?',
                'choices': [
                    ('By setting the reward to zero after a fixed number of steps.', False),
                    ('By using a discount rateγwhere0≤γ≤1in the sumgk=∑i=0∞γirk+i+1.', True),
                    ('By calculating the average of all rewards received until timek.', False),
                    ('By only considering the terminal stepNof the sequence.', False),
                ]
            },
            {
                'text': 'During error analysis, if you find an anomalous example that the model incorrectly assigns a high probabilityp(x), what is the suggested corrective action?',
                'choices': [
                    ('Try to identify or create a new feature that takes on an unusually large or small value for that specific anomaly.', True),
                    ('Decrease the size of the training setm.', False),
                    ('Always switch to a Supervised Learning algorithm like a Neural Network.', False),
                    ('Assume the anomaly is actually a normal example and ignore the error.', False),
                ]
            },
            {
                'text': 'Which metric is commonly used to evaluate anomaly detection systems when dealing with imbalanced classes?',
                'choices': [
                    ('F1-score', True),
                    ('Mean squared error', False),
                    ('Accuracy', False),
                    ('R-squared', False),
                ]
            },
            {
                'text': 'Because anomaly detection often involves highly imbalanced datasets (very few anomalies), which set of metrics is more appropriate for evaluation than simple classification accuracy?',
                'choices': [
                    ('Precision, Recall, andF1-score.', True),
                    ('Mean Squared Error andR2.', False),
                    ('The value of the learning rateα.', False),
                    ('The number of featuresndivided bym.', False),
                ]
            },
            {
                'text': 'In the context of theExploration-Exploitation dilemma, what does "Exploitation" refer to?',
                'choices': [
                    ("Maximizing the current reward using the agent's limited current information.", True),
                    ('Moving to unknown states to gather more information about the environment.', False),
                    ('Reducing the discount rateγto zero.', False),
                    ('Identifying the stochastic components of the reward model.', False),
                ]
            },
            {
                'text': 'In anomaly detection for monitoring systems, why might new features like ratios of existing features be created?',
                'choices': [
                    ('To capture unusual relationships that indicate anomalies', True),
                    ('To reduce the number of dimensions in the data', False),
                    ('To normalize all features to the same scale', False),
                    ('To increase the variance in the dataset', False),
                ]
            },
            {
                'text': 'If a featurexused in an anomaly detection algorithm has a non-Gaussian (skewed) distribution, which of the following is a common practice to improve the model performance?',
                'choices': [
                    ('Apply a transformation likelog(x)orxto make the data look more Gaussian.', True),
                    ('Discard the feature entirely as it cannot be used.', False),
                    ('Increase the thresholdϵto compensate for the skew.', False),
                    ('Only use the feature in a Supervised Learning model instead.', False),
                ]
            },
            {
                'text': 'To find a moviejthat is most similar to movieiafter learning feature vectors, which of the following criteria is used?',
                'choices': [
                    ('Finding the moviejwith the smallest distance||x(i)−x(j)||.', True),
                    ('Finding the moviejwith the highest star rating from Alice.', False),
                    ('Finding the moviejthat has the most total ratings in the dataset.', False),
                    ('Finding the moviejwith the largest parameter vectorθ.', False),
                ]
            },
            {
                'text': 'How are similar movies identified in a recommender system using learned feature vectors?',
                'choices': [
                    ('By finding moviesjwith small‖x(i)−x(j)‖for a given moviei', True),
                    ('By comparing user parameter vectorsθ(j)', False),
                    ('By summing the ratings across all users', False),
                    ('By maximizing the predicted ratings', False),
                ]
            },
            {
                'text': 'What is the probability density function for a univariate Gaussian distribution with meanμand varianceσ2?',
                'choices': [
                    ('12πσexp\u2061(−(x−μ)22σ2)', True),
                    ('12πσ2exp\u2061(−(x−μ)22σ)', False),
                    ('12πσexp\u2061(−(x−μ)2σ2)', False),
                    ('12πσexp\u2061(−(x+μ)22σ2)', False),
                ]
            },
            {
                'text': 'For a one-dimensional Gaussian distributionN(μ,σ2), what effect does increasing the standard deviationσhave on the probability density function plot?',
                'choices': [
                    ('The bell curve becomes wider and its peak height decreases.', True),
                    ('The bell curve becomes narrower and its peak height increases.', False),
                    ('The center of the bell curve shifts to the right along the x-axis.', False),
                    ('The area under the curve increases to become greater than 1.', False),
                ]
            },
            {
                'text': 'In gradient descent for recommender systems, what is the update rule forθk(j)whenk≠0?',
                'choices': [
                    ('θk(j):=θk(j)−α(∑i:r(i,j)=1((θ(j))Tx(i)−y(i,j))xk(i)+λθk(j))', True),
                    ('θk(j):=θk(j)+α(∑i:r(i,j)=1((θ(j))Tx(i)−y(i,j))xk(i)+λθk(j))', False),
                    ('θk(j):=θk(j)−α∑i:r(i,j)=1((θ(j))Tx(i)+y(i,j))xk(i)', False),
                    ('θk(j):=θk(j)−αλ∑k=1nθk(j)', False),
                ]
            },
            {
                'text': 'According to empirical studies on large-scale machine learning, such as those by Banko and Brill, what is often the most decisive factor in achieving high accuracy for tasks like natural language disambiguation?',
                'choices': [
                    ('Choosing a complex non-linear kernel for a Support Vector Machine.', False),
                    ('Increasing the volume of training data significantly, regardless of the specific algorithm used.', True),
                    ('Manually engineering highly specific features for the dataset.', False),
                    ('Reducing the number of parameters to prevent overfitting.', False),
                ]
            },
            {
                'text': 'What is the first step in the collaborative filtering algorithm?',
                'choices': [
                    ('Initializex(1),…,x(nm),θ(1),…,θ(nu)to small random values', True),
                    ('Set all parameters to zero', False),
                    ('Use predefined feature vectors for items', False),
                    ('Normalize all ratings to mean zero', False),
                ]
            },
            {
                'text': 'To force Stochastic Gradient Descent to converge to a single point rather than oscillating near the minimum, one might use a learning rateαthat:',
                'choices': [
                    ('Increases as the number of iterations increases.', False),
                    ('Slowly decreases over time, for example, using a formula likeα=const1iterationNumber+const2.', True),
                    ('Remains strictly constant throughout the entire training process.', False),
                    ('Is calculated as the average of all previous gradients.', False),
                ]
            },
            {
                'text': 'In recommender systems, what does low rank matrix factorization refer to?',
                'choices': [
                    ('Decomposing the ratings matrixYinto user parametersΘand item featuresXsuch thatY≈XΘT', True),
                    ('Reducing the rank of the feature matrix only', False),
                    ('Increasing the dimensions of the parameter vectors', False),
                    ('Applying SVD directly to the ratings matrix without optimization', False),
                ]
            },
            {
                'text': 'The collaborative filtering algorithm is also known as "Low Rank Matrix Factorization." This is because the matrix of predicted ratings can be expressed as:',
                'choices': [
                    ('The product of the feature matrixXand the transpose of the parameter matrixθT.', True),
                    ('The sum of the movie features and the user ratings.', False),
                    ('The inverse of the rating matrixY.', False),
                    ('A diagonal matrix containing only the mean ratings.', False),
                ]
            },
            {
                'text': 'How isReinforcement Learningdistinct from Supervised Learning in the context of data processing?',
                'choices': [
                    ('It relies on clustering and dimension reduction of inputs.', False),
                    ('It requires a supervisor to provide the correct output for every input.', False),
                    ('It learns through trial and error interactions to maximize a reward signal without a direct supervisor.', True),
                    ('It is limited only to processing i.i.d. (independent and identically distributed) data streams.', False),
                ]
            },
            {
                'text': 'What is the core requirement for a learning algorithm to be successfully parallelized using the Map-Reduce framework?',
                'choices': [
                    ('It must be a deep neural network with at least five layers.', False),
                    ('The main computation must be expressible as a summation over the training set.', True),
                    ('It must use a decreasing learning rateαover time.', False),
                    ('The dataset must be small enough to fit into the RAM of a single machine.', False),
                ]
            },
            {
                'text': 'What is the defining property of anInformation State(or Markov State)Xk?',
                'choices': [
                    ('The future is independent of the past given the present:P[Xk+1|Xk]=P[Xk+1|X0,...,Xk].', True),
                    ('The state must include the entire historyHkin its raw form.', False),
                    ('The state must be a discrete integer value.', False),
                    ('The state is fully visible to the agent at all times.', False),
                ]
            },
            {
                'text': 'How is the meanμjestimated for thej-th feature in anomaly detection using Gaussian distributions?',
                'choices': [
                    ('μj=1m∑i=1mxj(i)', True),
                    ('μj=1m∑i=1m(xj(i))2', False),
                    ('μj=m∑i=1mxj(i)', False),
                    ('μj=1m∑i=1mxj(i)', False),
                ]
            },
            {
                'text': 'Why is mean normalization used in recommender systems?',
                'choices': [
                    ('To handle users who have not rated any items or to improve convergence', True),
                    ('To increase the variance of the ratings', False),
                    ('To eliminate the regularization term', False),
                    ('To set all missing ratings to zero', False),
                ]
            },
            {
                'text': 'What is the primary purpose of applying Mean Normalization to the rating matrixY?',
                'choices': [
                    ('To ensure that users who have not rated any movies receive a predicted rating equal to the average rating for those movies.', True),
                    ('To reduce the number of featuresnrequired for the model.', False),
                    ('To eliminate the need for the regularization parameterλ.', False),
                    ('To convert all star ratings into a binary 0 or 1 format.', False),
                ]
            },
            {
                'text': 'When dealing with highly imbalanced datasets where the positive class is rare, which evaluation metric is generally considered more informative than standard accuracy or ROC-AUC?',
                'choices': [
                    ('Mean Squared Error (MSE) [cite: 966]', False),
                    ('Coefficient of DeterminationR2[cite: 966]', False),
                    ('Precision-Recall AUC (PR-AUC) [cite: 965, 967]', True),
                    ('Mean Absolute Error (MAE) [cite: 966, 967]', False),
                ]
            },
            {
                'text': 'What is a primary advantage of Mini-batch Gradient Descent over pure Stochastic Gradient Descent?',
                'choices': [
                    ('It guarantees convergence to the global minimum in fewer iterations.', False),
                    ('It allows for vectorized implementations that can leverage hardware speedups.', True),
                    ('It eliminates the need for a learning rateα.', False),
                    ('It uses the entire dataset to calculate the gradient, ensuring a smooth path.', False),
                ]
            },
            {
                'text': 'In a production machine learning system, which components are responsible for closing the loop between real-world performance and model refinement?',
                'choices': [
                    ('Evaluation and Monitoring [cite: 902, 911, 917]', True),
                    ('Feature Engineering and Training [cite: 902]', False),
                    ('Data Collection and Cleaning [cite: 902]', False),
                    ('Problem Framing and Deployment [cite: 902]', False),
                ]
            },
            {
                'text': "Which type of machine learning security attack involves corrupting the training data or labels to influence the resulting model's behavior?",
                'choices': [
                    ('Adversarial examples [cite: 1271, 1285]', False),
                    ('Data poisoning [cite: 1272, 1286]', True),
                    ('Model extraction [cite: 1273, 1287]', False),
                    ('Input injection [cite: 1274]', False),
                ]
            },
            {
                'text': 'How is convergence typically monitored when using Stochastic Gradient Descent on a large dataset?',
                'choices': [
                    ('By calculating the total costJtrain(θ)over allmexamples after every update.', False),
                    ('By plotting the average cost of the last 1,000 (or similar) examples processed.', True),
                    ('By checking if the parameterθbecomes exactly zero.', False),
                    ('By only measuring the error on the final training example.', False),
                ]
            },
            {
                'text': 'What is the formula for the multivariate Gaussian probability density function?',
                'choices': [
                    ('p(x;μ,Σ)=1(2π)n/2|Σ|1/2exp\u2061(−12(x−μ)TΣ−1(x−μ))', True),
                    ('p(x;μ,Σ)=1(2π)n|Σ|exp\u2061(−12(x−μ)TΣ(x−μ))', False),
                    ('p(x;μ,Σ)=(2π)n/2|Σ|1/2exp\u2061(12(x−μ)TΣ−1(x−μ))', False),
                    ('p(x;μ,Σ)=1(2π)n/2|Σ|1/2exp\u2061(12(x−μ)TΣ−1(x−μ))', False),
                ]
            },
            {
                'text': 'What is the primary advantage of using a Multivariate Gaussian distribution over the original (independent) Gaussian model for anomaly detection?',
                'choices': [
                    ('It can automatically capture correlations between different features.', True),
                    ('It is computationally much cheaper to calculate for very large numbers of features.', False),
                    ('It works even if the training set sizemis smaller than the number of featuresn.', False),
                    ('It does not require the calculation of the mean vectorμ.', False),
                ]
            },
            {
                'text': 'What is the primary purpose of utilizing aNested Cross-Validationprotocol during the model selection phase?',
                'choices': [
                    ('To increase the size of the available training data [cite: 943]', False),
                    ('To avoid optimistic bias by separating hyperparameter tuning from final generalization estimation [cite: 951, 955, 958]', True),
                    ('To ensure that random seeds remain fixed across iterations [cite: 1013]', False),
                    ('To minimize the computational cost of training many model families [cite: 945]', False),
                ]
            },
            {
                'text': 'Which term describes a scenario where an agent doesnothave full access to the environment statexk, often requiring the reconstruction of state information?',
                'choices': [
                    ('Markov Decision Process (MDP)', False),
                    ('Partially Observable Markov Decision Process (POMDP)', True),
                    ('Linear Time-Invariant (LTI) process', False),
                    ('Deterministic Policy Mapping', False),
                ]
            },
            {
                'text': "In an 'Online Learning' setting, such as a website predicting Click-Through Rate (CTR), what happens after an update is made using a specific user's data(x,y)?",
                'choices': [
                    ('The data point is typically discarded and never reused.', True),
                    ('The data point is added to a permanent database for batch processing later.', False),
                    ('The algorithm halts until more data points arrive to form a mini-batch.', False),
                    ('The learning rateαis reset to its initial value.', False),
                ]
            },
            {
                'text': 'What is the optimization objective for learning the parameter vectorθ(j)for a single user in a content-based recommender system?',
                'choices': [
                    ('minθ(j)∑i:r(i,j)=1((θ(j))Tx(i)−y(i,j))2+λ∑k=1n(θk(j))2', True),
                    ('maxθ(j)∑i:r(i,j)=1((θ(j))Tx(i)−y(i,j))2+λ∑k=1n(θk(j))2', False),
                    ('minθ(j)∑i:r(i,j)=0((θ(j))Tx(i)−y(i,j))2', False),
                    ('minθ(j)∏i:r(i,j)=1((θ(j))Tx(i)−y(i,j))2', False),
                ]
            },
            {
                'text': 'How does a collaborative filtering algorithm typically learn the parametersθand the featuresx?',
                'choices': [
                    ('By minimizing a combined cost functionJthat updates bothθandxsimultaneously.', True),
                    ('By keepingθfixed at all times and only varyingx.', False),
                    ('By randomly guessing values until the error reaches zero.', False),
                    ('By ignoring users who have rated fewer than 10 movies.', False),
                ]
            },
            {
                'text': 'When fitting a Gaussian distribution to a dataset{x(1),...,x(m)}, which formula is commonly used to estimate the varianceσ2?',
                'choices': [
                    ('σ2=1m∑i=1m(x(i)−μ)2', True),
                    ('σ2=1m∑i=1mx(i)', False),
                    ('σ2=1m∑i=1m(x(i)−μ)', False),
                    ('σ2=∑i=1m(x(i)−μ)2', False),
                ]
            },
            {
                'text': 'AStochastic Policyis defined as:',
                'choices': [
                    ('A direct mapping where an action is always determined by the state:uk=π(xk).', False),
                    ('A mapping of the probability of an action given a state:π(Uk|Xk)=P[Uk|Xk].', True),
                    ('An internal model that predicts the next rewardRk+1.', False),
                    ('A fixed set of rules that never change over time.', False),
                ]
            },
            {
                'text': 'When using Mean Normalization, the final predicted rating for userjon movieiis calculated as:',
                'choices': [
                    ('(θ(j))T(x(i))+μi', True),
                    ('(θ(j))T(x(i))−μi', False),
                    ('μi÷(θ(j))T(x(i))', False),
                    ('(θ(j))T×(μi+x(i))', False),
                ]
            },
            {
                'text': 'In decision-making systems based on risk levels, why iscalibrationconsidered essential even if a model has high ranking performance?',
                'choices': [
                    ("It improves the model's accuracy on rare classes [cite: 962]", False),
                    ('It ensures that the predicted probability scores are trustworthy and reflect actual observed frequencies [cite: 979, 980, 990, 996]', True),
                    ('It prevents the model from being extracted by adversarial queries [cite: 1273]', False),
                    ('It automatically selects the optimal decision thresholdτ[cite: 971, 972]', False),
                ]
            },
            {
                'text': 'In anomaly detection using independent Gaussian assumptions, how isp(x)computed for a new examplex?',
                'choices': [
                    ('p(x)=∏j=1np(xj;μj,σj2)', True),
                    ('p(x)=∑j=1np(xj;μj,σj2)', False),
                    ('p(x)=∏j=1n(xj−μj)2', False),
                    ('p(x)=∑j=1n1σj2', False),
                ]
            },
            {
                'text': 'Which statement best captures the core objective of reinforcement learning?',
                'choices': [
                    ('Learn a strategy that maximizes expected long-term reward through interaction with an environment.', True),
                    ('Infer labels for unlabeled data by clustering similar inputs.', False),
                    ('Fit a model only by minimizing training error on i.i.d. labeled examples.', False),
                    ('Guarantee optimal decisions without any feedback signal.', False),
                ]
            },
            {
                'text': 'In many machine learning applications, what is a common effect of increasing the training set size (while keeping the model class and feature set fixed)?',
                'choices': [
                    ('It often improves generalization performance, reducing error up to a point.', True),
                    ('It guarantees zero test error for any learning algorithm.', False),
                    ('It always causes overfitting to increase.', False),
                    ('It makes feature engineering unnecessary in all cases.', False),
                ]
            },
            {
                'text': 'In a standard ML workflow, what is the primary purpose of thetestset?',
                'choices': [
                    ('To provide a final, unbiased estimate of generalization after model selection is complete.', True),
                    ('To tune hyperparameters such as learning rate and regularization strength.', False),
                    ('To increase the training data size for better fitting.', False),
                    ('To ensure the model achieves zero error before deployment.', False),
                ]
            },
            {
                'text': 'Which option correctly distinguishesdata driftfromconcept drift?',
                'choices': [
                    ('Data drift:p(x)changes; concept drift:p(y∣x)changes.', True),
                    ('Data drift:p(y∣x)changes; concept drift:p(x)changes.', False),
                    ('Both mean only that the training loss decreased over time.', False),
                    ('Concept drift occurs only in regression, data drift only in classification.', False),
                ]
            },
            {
                'text': "Many learning algorithms can be written as computing a sum over training examples. In a MapReduce-style approach, what is the typical role of the 'reduce' (combine) step?",
                'choices': [
                    ('Aggregate partial sums (e.g., partial gradients) computed on different data partitions into a final combined result.', True),
                    ('Randomly permute the dataset to improve generalization.', False),
                    ('Choose the learning rateαautomatically without evaluation.', False),
                    ('Convert a supervised task into an unsupervised one.', False),
                ]
            },
            {
                'text': 'What is the main difference between the state-value functionvπ(x)and the action-value functionqπ(x,u)?',
                'choices': [
                    ('vπ(x)is the expected return starting from statexfollowingπ;qπ(x,u)conditions on first taking actionuinxthen followingπ.', True),
                    ('vπ(x)is defined only for episodic tasks;qπ(x,u)only for continuing tasks.', False),
                    ('qπ(x,u)ignores rewards and only models transitions.', False),
                    ('vπ(x)requires a known environment model, butqπ(x,u)never does.', False),
                ]
            },
            {
                'text': 'In a standard agent-environment loop at time stepk, what does the agent typically receive from the environment after choosing an actionuk?',
                'choices': [
                    ('An observation (e.g.,yk+1) and a reward (e.g.,rk+1).', True),
                    ('The true optimal policyπ∗for the task.', False),
                    ('A full dataset of labeled examples for supervised learning.', False),
                    ('Only the next state, but never a reward signal.', False),
                ]
            },
            {
                'text': 'Which statement best describesbatch gradient descentcompared tostochastic gradient descent?',
                'choices': [
                    ('Batch gradient descent uses allmtraining examples to compute one parameter update.', True),
                    ('Batch gradient descent uses exactly one example to compute each update.', False),
                    ('Stochastic gradient descent requires solving a linear system exactly each step.', False),
                    ('Stochastic gradient descent cannot be used for linear regression.', False),
                ]
            },
            {
                'text': 'Which situation is the clearest example ofdata leakageduring model evaluation?',
                'choices': [
                    ('Using information derived from future outcomes (or test data) in feature construction for training.', True),
                    ('Training a model with too many parameters relative to dataset size.', False),
                    ('Shuffling the training data before running SGD.', False),
                    ('Evaluating with a confusion matrix instead of accuracy.', False),
                ]
            },
            {
                'text': 'Mini-batch gradient descent updates parameters using:',
                'choices': [
                    ('A small subset ofbexamples per iteration (with1<b<m).', True),
                    ('Only one randomly chosen feature per iteration.', False),
                    ('All possible subsets of the data in each iteration.', False),
                    ('The entire dataset but without computing gradients.', False),
                ]
            },
            {
                'text': 'The reward hypothesis states that goals can be described as:',
                'choices': [
                    ('Maximizing the expected cumulative rewardE[∑i=0∞Rk+i+1].', True),
                    ('Maximizing the number of actions taken per episode regardless of outcome.', False),
                    ('Minimizing the variance of observationsykwithout using rewards.', False),
                    ('Selecting actions uniformly at random to avoid bias.', False),
                ]
            },
            {
                'text': 'Why is a time-based split often preferred for forecasting problems?',
                'choices': [
                    ('It helps prevent temporal leakage by ensuring training data comes from earlier times than evaluation data.', True),
                    ('It guarantees that classes are perfectly balanced across splits.', False),
                    ('It makes cross-validation unnecessary in all cases.', False),
                    ('It eliminates the need for feature engineering.', False),
                ]
            },
            {
                'text': 'What is the main advantage ofnested cross-validationwhen performing heavy model or hyperparameter search?',
                'choices': [
                    ('It reduces optimistic bias by separating hyperparameter tuning from final generalization estimation.', True),
                    ('It always produces higher accuracy than any single split.', False),
                    ('It guarantees the selected model is globally optimal across all possible algorithms.', False),
                    ('It prevents overfitting by forcingα=0.', False),
                ]
            },
            {
                'text': 'For continuing (infinite-horizon) tasks, a common definition of return is:',
                'choices': [
                    ('Gk=∑i=0∞γirk+i+1with0≤γ≤1.', True),
                    ('Gk=rk+1only, ignoring all future rewards.', False),
                    ('Gk=∑i=0Nrk+i+1whereNis always finite even when the task never ends.', False),
                    ('Gk=γ−krkto amplify distant rewards.', False),
                ]
            },
            {
                'text': 'Why is it common practice to randomly shuffle (reorder) training examples when using stochastic gradient descent?',
                'choices': [
                    ('To reduce harmful ordering effects and make successive updates more representative.', True),
                    ('To ensure the cost function becomes exactly quadratic.', False),
                    ('To eliminate the need for a learning rateα.', False),
                    ('To force the gradient to be zero at every step.', False),
                ]
            },
            {
                'text': 'In a classification problem with severe class imbalance, why can accuracy be misleading?',
                'choices': [
                    ('A model can predict the majority class most of the time and still achieve high accuracy while missing rare positives.', True),
                    ('Accuracy is undefined unlessy∈{−1,+1}.', False),
                    ('Accuracy depends only on true positives, not true negatives.', False),
                    ('Accuracy automatically accounts for different misclassification costs.', False),
                ]
            },
            {
                'text': 'When monitoring convergence of stochastic gradient descent, a practical approach is to:',
                'choices': [
                    ('Plot an average of the recent values ofcost(θ,(x(i),y(i)))over a window of examples.', True),
                    ('Check whether the training error becomes exactly zero after each update.', False),
                    ('Stop only when the gradient is symbolically equal to0for all parameters.', False),
                    ('Monitor only the first parameterθ0; others always converge ifθ0converges.', False),
                ]
            },
            {
                'text': 'How does the discount factorγtypically affect an agent’s behavior?',
                'choices': [
                    ('Ifγ≈1the agent is more far-sighted; ifγ≈0it focuses on immediate reward.', True),
                    ('Ifγ≈1the agent ignores future rewards; ifγ≈0it values the future more.', False),
                    ('γonly changes the action space size, not the preference for future rewards.', False),
                    ('γmust always be greater than 1 for stable learning.', False),
                ]
            },
            {
                'text': 'Which learning-rate strategy is commonly used to help stochastic gradient descent converge?',
                'choices': [
                    ('Start with a reasonableα, and optionally decrease it over time (e.g.,α=const1iterationNumber+const2).', True),
                    ('Increaseαsteadily over time to guarantee faster convergence.', False),
                    ('Setα=0after a few iterations to prevent noise.', False),
                    ('Use a negativeαto move against the objective function.', False),
                ]
            },
            {
                'text': 'A stateXkis called a Markov (information) state when:',
                'choices': [
                    ('P[Xk+1∣Xk]=P[Xk+1∣X0,X1,…,Xk].', True),
                    ('Xkequals the entire historyHkand cannot be compressed.', False),
                    ('P[Xk+1∣Xk]=0for all transitions except one.', False),
                    ('Xkcontains only rewards and never observations or dynamics information.', False),
                ]
            },
            {
                'text': 'For rare-positive (highly imbalanced) classification, which metric is often more informative about performance on positives?',
                'choices': [
                    ('PR-AUC (precision-recall area under curve).', True),
                    ('ROC-AUC only, because it always focuses on rare positives.', False),
                    ('Raw accuracy, because it is threshold-independent.', False),
                    ('Mean squared error (MSE), because it is robust to imbalance.', False),
                ]
            },
            {
                'text': 'If the environment state is Markov but the agent cannot directly observe it fully, the problem is commonly modeled as a:',
                'choices': [
                    ('Partially Observable Markov Decision Process (POMDP).', True),
                    ('Fully Observable Markov Decision Process (MDP) by definition.', False),
                    ('Purely supervised learning (since the state is Markov).', False),
                    ('Deterministic planning (since observability is irrelevant).', False),
                ]
            },
            {
                'text': 'Which scenario best matchesonline learning?',
                'choices': [
                    ('Continuously updatingθas new data(x,y)arrives, adapting to changing patterns.', True),
                    ('Training once on a fixed dataset and never updating the model again.', False),
                    ('Only updating the model after collecting all data for a year.', False),
                    ('Using only unsupervised learning methods without labels.', False),
                ]
            },
            {
                'text': 'Many classifiers output a score or probability estimatep(y=1∣x). What does choosing a thresholdτprimarily control?',
                'choices': [
                    ('The tradeoff between false positives and false negatives, turning scores into actions.', True),
                    ('The number of model parametersθused during training.', False),
                    ('Whether the model becomes linear or non-linear.', False),
                    ('The feature dimensionality used in preprocessing.', False),
                ]
            },
            {
                'text': 'Which choice correctly contrasts common action space types in reinforcement learning?',
                'choices': [
                    ('Finite action set:uk∈{uk,1,uk,2,…}; continuous action set:uk∈Rm.', True),
                    ('Finite action set:uk∈Rm; continuous action set:uk∈{N,E,S,W}.', False),
                    ('Finite action set requiresγ=0; continuous action set requiresγ=1.', False),
                    ('Action spaces are always continuous in reinforcement learning.', False),
                ]
            },
            {
                'text': 'For a binary classification problem withy∈{0,1}, which expression represents the model’s predicted probability in many standard classifiers (e.g., logistic regression)?',
                'choices': [
                    ('p(y=1∣x;θ).', True),
                    ('p(x=1∣y;θ).', False),
                    ('∑i=1my(i).', False),
                    ('θ⊤θ(independent ofx).', False),
                ]
            },
            {
                'text': 'What does it mean for a probabilistic classifier to be well-calibrated?',
                'choices': [
                    ('Among examples predicted with probabilityp, the observed frequency ofy=1is approximatelyp.', True),
                    ('Its ROC-AUC is exactly 1.0 on the training set.', False),
                    ('It always assigns probabilities of 0 or 1 only.', False),
                    ('Calibration means the model uses the sameθvalues for every dataset.', False),
                ]
            },
            {
                'text': 'In large-scale learning, data parallelism is primarily about:',
                'choices': [
                    ('Splitting training examples across multiple machines/cores to compute partial results in parallel, then combining them.', True),
                    ('Training separate models for each feature and never combining them.', False),
                    ('Encrypting data so that no machine can read it.', False),
                    ('Reducing dimensionality by removing parallel features.', False),
                ]
            },
            {
                'text': 'Which statement correctly describes deterministic vs. stochastic policies?',
                'choices': [
                    ('Deterministic:uk=π(xk); stochastic:π(Uk∣Xk)=P[Uk∣Xk].', True),
                    ('Deterministic:π(Uk∣Xk)is always uniform; stochastic:uk=π(xk)always.', False),
                    ('Deterministic policies can only be used with POMDPs; stochastic policies only with fully observable MDPs.', False),
                    ('Policies map rewards to states, not states to actions.', False),
                ]
            },
            {
                'text': 'Which issue best describestraining-serving skewin deployed ML systems?',
                'choices': [
                    ('The preprocessing or feature logic differs between training and inference, causing inconsistent model inputs.', True),
                    ('The model is too small to fit the training data.', False),
                    ('The GPU is underutilized during offline training.', False),
                    ('The confusion matrix is symmetric by construction.', False),
                ]
            },
            {
                'text': 'Which topic in reinforcement learning involves combining elements of dynamic programming and Monte Carlo methods?',
                'choices': [
                    ('Temporal difference learning', True),
                    ('Markov decision processes', False),
                    ('Policy gradient methods', False),
                    ('Function approximation', False),
                ]
            },
            {
                'text': 'In machine learning tasks such as classifying confusable words, what often determines the winner among different algorithms?',
                'choices': [
                    ('The one with the most data', True),
                    ('The one with the most complex algorithm', False),
                    ('The one with the highest computational power', False),
                    ('The one with the fewest features', False),
                ]
            },
            {
                'text': 'In practice, a machine learning model is considered as what in a larger pipeline?',
                'choices': [
                    ('One component', True),
                    ('The entire system', False),
                    ('A standalone algorithm', False),
                    ('Only the data processor', False),
                ]
            },
            {
                'text': 'Many machine learning algorithms involve computing sums over the training set, which can be parallelized using what technique?',
                'choices': [
                    ('Map-reduce', True),
                    ('Stochastic shuffling', False),
                    ('Batch normalization', False),
                    ('Learning rate decay', False),
                ]
            },
            {
                'text': 'What is an example of an ML-specific security attack where inputs are crafted to cause mispredictions?',
                'choices': [
                    ('Adversarial examples', True),
                    ('Data augmentation', False),
                    ('Feature selection', False),
                    ('Hyperparameter tuning', False),
                ]
            },
            {
                'text': 'In comparing reinforcement learning and model predictive control, which approach inherently handles adaptivity without requiring additional components?',
                'choices': [
                    ('Reinforcement learning', True),
                    ('Model predictive control', False),
                    ('Both equally', False),
                    ('Neither', False),
                ]
            },
            {
                'text': 'When does adding more training examples to a machine learning model typically reduce the training error significantly?',
                'choices': [
                    ('When the model has high variance', True),
                    ('When the model has high bias', False),
                    ('When the learning rate is too high', False),
                    ('When the dataset is already small', False),
                ]
            },
            {
                'text': 'What is the purpose of the test set in machine learning data splits?',
                'choices': [
                    ('Final estimate of generalization', True),
                    ('Fitting parameters', False),
                    ('Choosing hyperparameters', False),
                    ('Training the model', False),
                ]
            },
            {
                'text': 'According to common definitions, how many types of reinforcement are there, including positive, negative, extinction, and punishment?',
                'choices': [
                    ('Four', True),
                    ('Two', False),
                    ('Three', False),
                    ('Five', False),
                ]
            },
            {
                'text': 'In batch gradient descent for linear regression, how is the parameterθjupdated in each iteration?',
                'choices': [
                    ('θj:=θj−α1m∑i=1m(hθ(x(i))−y(i))xj(i)', True),
                    ('θj:=θj−α(hθ(x(i))−y(i))xj(i)for a single i', False),
                    ('θj:=θj+α1m∑i=1m(hθ(x(i))−y(i))xj(i)', False),
                    ('θj:=θj−α∑i=1m(hθ(x(i))−y(i))', False),
                ]
            },
            {
                'text': 'When is nested cross-validation particularly useful?',
                'choices': [
                    ('For small datasets and heavy hyperparameter search', True),
                    ('Only for large datasets', False),
                    ('When no hyperparameters are involved', False),
                    ('For real-time deployment', False),
                ]
            },
            {
                'text': 'Who is associated with the development of classical conditioning, a foundational concept in reinforcement learning?',
                'choices': [
                    ('Ivan Pavlov', True),
                    ('Andrei Markov', False),
                    ('Richard Bellman', False),
                    ('Andrew Barto', False),
                ]
            },
            {
                'text': 'Which of the following is an example of a contemporary application of reinforcement learning?',
                'choices': [
                    ('Playing the strategy board game Go at super-human performance', True),
                    ('Classifying images in supervised learning', False),
                    ('Clustering data points', False),
                    ('Performing linear regression', False),
                ]
            },
            {
                'text': 'For classification problems with rare positive classes, which metric is often more informative?',
                'choices': [
                    ('PR-AUC', True),
                    ('Accuracy', False),
                    ('MSE', False),
                    ('R-squared', False),
                ]
            },
            {
                'text': 'What is the first step in implementing stochastic gradient descent?',
                'choices': [
                    ('Randomly shuffle the training examples', True),
                    ('Compute the full gradient over all examples', False),
                    ('Increase the learning rate', False),
                    ('Plot the cost function', False),
                ]
            },
            {
                'text': 'Which variant of gradient descent uses all training examples in each iteration?',
                'choices': [
                    ('Batch gradient descent', True),
                    ('Stochastic gradient descent', False),
                    ('Mini-batch gradient descent', False),
                    ('Online gradient descent', False),
                ]
            },
            {
                'text': 'According to the reward hypothesis, all goals can be described by maximizing the expected value of what?',
                'choices': [
                    ('Cumulative reward', True),
                    ('Immediate reward only', False),
                    ('State transitions', False),
                    ('Action probabilities', False),
                ]
            },
            {
                'text': "How is a binary decision typically made from a model's probability outputp(y=1|x)?",
                'choices': [
                    ('Using a thresholdτ]>', True),
                    ('Directly as the output', False),
                    ('Through random sampling', False),
                ]
            },
            {
                'text': 'In mini-batch gradient descent, if the mini-batch sizeb=10, how many examples are used to compute the gradient in each update?',
                'choices': [
                    ('10', True),
                    ('1', False),
                    ('All m examples', False),
                    ('100', False),
                ]
            },
            {
                'text': 'Which method is commonly used for calibrating probabilities in deep neural networks?',
                'choices': [
                    ('Temperature scaling', True),
                    ('Random forest aggregation', False),
                    ('K-means clustering', False),
                    ('Principal component analysis', False),
                ]
            },
            {
                'text': 'In continuing tasks without a natural end, the return is typically defined using what to prevent infinite values?',
                'choices': [
                    ('Discounting', True),
                    ('Summation without limits', False),
                    ('Multiplication by a constant', False),
                    ('Averaging over episodes', False),
                ]
            },
            {
                'text': 'What is a key advantage of mini-batch gradient descent over stochastic gradient descent when using vectorization?',
                'choices': [
                    ('Faster computation due to processing multiple examples at once', True),
                    ('Slower convergence', False),
                    ('Requires shuffling after each update', False),
                    ('Uses the entire dataset per iteration', False),
                ]
            },
            {
                'text': 'A state is called an information state if the probability of the next state depends only on the current state and not on the entire history, satisfying which condition?',
                'choices': [
                    ('P[Xk+1|Xk]=P[Xk+1|X0,X1,…,Xk]', True),
                    ('P[Xk+1|Xk]=P[Xk|Xk+1]', False),
                    ('E[Xk+1]=Xk', False),
                    ('Xk+1=f(Xk)deterministically', False),
                ]
            },
            {
                'text': 'What is a common cause of training-serving skew in machine learning pipelines?',
                'choices': [
                    ('Different preprocessing between training and inference', True),
                    ('Identical feature definitions', False),
                    ('Consistent missing-value handling', False),
                    ('Same tokenization methods', False),
                ]
            },
            {
                'text': 'What does concept drift refer to in deployed machine learning models?',
                'choices': [
                    ('Changes inp(y|x)', True),
                    ('Changes inp(x)', False),
                    ('Stable input distributions', False),
                    ('Constant relationships', False),
                ]
            },
            {
                'text': 'How can convergence be checked in stochastic gradient descent?',
                'choices': [
                    ('Plot the average cost over the last k examples processed', True),
                    ('Plot the full training cost after each example', False),
                    ('Increase the learning rate until it diverges', False),
                    ('Compute the gradient norm only once', False),
                ]
            },
            {
                'text': 'What does a stochastic policy map in reinforcement learning?',
                'choices': [
                    ('The probability of an action given a state', True),
                    ('A state directly to an action', False),
                    ('Rewards to states', False),
                    ('Actions to rewards', False),
                ]
            },
            {
                'text': 'Which fairness criterion requires equal true positive rates and false positive rates across groups?',
                'choices': [
                    ('Equalized odds', True),
                    ('Demographic parity', False),
                    ('Predictive parity', False),
                    ('Individual fairness', False),
                ]
            },
            {
                'text': 'In online learning, how are model parameters typically updated?',
                'choices': [
                    ('Using each new example as it arrives', True),
                    ('Using batches of historical data only', False),
                    ('Only after collecting all data', False),
                    ('Without any updates during runtime', False),
                ]
            },
            {
                'text': 'The action-value functionqπ(xk,uk)represents the expected return starting from a state, taking a specific action, and then following policyπ. What is its mathematical expression assuming an MDP?',
                'choices': [
                    ('Eπ[∑i=0∞γiRk+i+1|xk,uk]', True),
                    ('Eπ[Gk|Xk=xk]', False),
                    ('∑i=0∞rk+i+1', False),
                    ('P[Uk|Xk]', False),
                ]
            },
            {
                'text': 'In a typical recommender system problem formulation, what does the notationr(i,j)=1represent?',
                'choices': [
                    ('Userjhas provided a rating for moviei.', True),
                    ('Movieiis a romantic genre film.', False),
                    ('The predicted rating for userjon movieiis exactly 1 star.', False),
                    ('Userjhas never seen moviei.', False),
                ]
            },
            {
                'text': 'In recommender systems for movie ratings, what doesr(i,j)represent?',
                'choices': [
                    ('1 if userjhas rated moviei, 0 otherwise', True),
                    ('The rating given by userjto moviei', False),
                    ('The feature vector for moviei', False),
                    ('The parameter vector for userj', False),
                ]
            },
            {
                'text': 'In the collaborative filtering cost function, what role does the termλ2∑(θk(j))2play?',
                'choices': [
                    ('It acts as a regularization term to prevent the parameters from becoming too large and overfitting the data.', True),
                    ('It calculates the average rating across all movies.', False),
                    ('It measures the similarity between two different users.', False),
                    ('It represents the total number of users in the systemnu.', False),
                ]
            },
            {
                'text': 'Which of the following is a key difference betweenModel Predictive Control (MPC)and standardReinforcement Learning (RL)?',
                'choices': [
                    ('RL requires an a priori model, whereas MPC does not.', False),
                    ('MPC maximizes return, while RL minimizes costs.', False),
                    ('MPC inherently handles system constraints, whereas RL typically handles them only indirectly via the reward function.', True),
                    ('RL stability theory is considered mature, while MPC stability theory is immature.', False),
                ]
            },
            {
                'text': 'In which deployment pattern does a model run alongside a production system to compare outputs without actually influencing any real-world decisions?',
                'choices': [
                    ('Canary deployment [cite: 1146]', False),
                    ('A/B testing [cite: 1147]', False),
                    ('Shadow mode [cite: 1145]', True),
                    ('Batch scoring [cite: 1035]', False),
                ]
            },
            {
                'text': 'In a recommender system with a sparse user-item rating matrix, what does an indicator valuer(i,j)=1typically mean?',
                'choices': [
                    ('Userjhas provided a rating for itemi.', True),
                    ('Userjdislikes itemiwith certainty.', False),
                    ('Itemibelongs to classj.', False),
                    ('The ratingy(i,j)is equal to 1 star.', False),
                ]
            },
            {
                'text': "A common content-based recommender predicts a user's rating usingy^(i,j)=(θ(j))Tx(i). What dox(i)andθ(j)represent in this expression?",
                'choices': [
                    ('x(i)is the feature vector for itemi, andθ(j)is the preference/parameter vector for userj.', True),
                    ('x(i)is the user ID embedding, andθ(j)is the item ID embedding.', False),
                    ('x(i)is a list of all ratings for itemi, andθ(j)is the list of all ratings by userj.', False),
                    ('x(i)is the regularization strength, andθ(j)is the learning rate.', False),
                ]
            },
            {
                'text': 'Many recommender models minimize squared error plus a term likeλ2∑kθk2. What is the main purpose of this regularization term?',
                'choices': [
                    ('To reduce overfitting by penalizing large parameter values.', True),
                    ('To guarantee that the predicted ratings are integers.', False),
                    ('To ensure every user rates every item.', False),
                    ('To make the training data matrix dense by filling missing values automatically.', False),
                ]
            },
            {
                'text': 'When minimizing a squared-error objective with anL2penaltyλ2∑kθk2, which additional term commonly appears in the gradient forθk?',
                'choices': [
                    ('+λθk', True),
                    ('+λ', False),
                    ('+θk2', False),
                    ('+λθk', False),
                ]
            },
            {
                'text': 'Which statement best distinguishes collaborative filtering from a purely content-based recommender?',
                'choices': [
                    ('Collaborative filtering infers user preferences and item characteristics from user-item interactions (ratings) rather than relying only on explicit item attributes.', True),
                    ('Collaborative filtering requires every item to have a manually engineered feature vector.', False),
                    ('Collaborative filtering only works for binary (like/dislike) feedback.', False),
                    ('Collaborative filtering does not use optimization; it is purely rule-based.', False),
                ]
            },
            {
                'text': 'In low-rank matrix factorization for recommender systems, a rating matrixYis approximated using latent factors. Which description is most accurate?',
                'choices': [
                    ('Each itemihas a latent feature vectorx(i)∈Rnand each userjhas parametersθ(j)∈Rn, soy^(i,j)≈(θ(j))Tx(i)withnrelatively small.', True),
                    ('Every user-item pair gets its own independent parameter, so no shared structure is needed.', False),
                    ('The method replaces ratings with their sorted order and predicts ranks only.', False),
                    ('The method assumesYmust be a square matrix with the same number of users and items.', False),
                ]
            },
            {
                'text': 'After learning item feature vectorsx(i), one way to find items similar to itemiis to:',
                'choices': [
                    ('Select itemsjthat minimize the distance‖x(i)−x(j)‖.', True),
                    ('Select itemsjthat maximize‖x(i)−x(j)‖.', False),
                    ('Select items with the largest item index valuej.', False),
                    ('Select items with the smallest number of observed ratings.', False),
                ]
            },
            {
                'text': 'Mean normalization for recommender systems often computes an average ratingμifor each item. After training a model on mean-normalized ratings, how is the final predicted rating commonly formed?',
                'choices': [
                    ('y^(i,j)=(θ(j))Tx(i)+μi', True),
                    ('y^(i,j)=(θ(j))Tx(i)−μi', False),
                    ("y^(i,j)=μjwhereμjis the user's mean rating.", False),
                    ('y^(i,j)=μionly, and the learned model is discarded.', False),
                ]
            },
            {
                'text': "Suppose a new user has provided no ratings yet. In a mean-normalized collaborative filtering system, what is a common behavior for that user's predictions before collecting any feedback?",
                'choices': [
                    ('Predictions tend to be close to item meansμi(because the user-specific term contributes little without data).', True),
                    ('Predictions become exactly 0 for every item, even after adding any baseline.', False),
                    ('Predictions become random integers between 1 and 5 by design.', False),
                    ("Predictions require computing similarities from that user's past ratings, so no predictions are possible.", False),
                ]
            },
            {
                'text': 'In many rating datasets, most user-item pairs are missing. Why is it generally incorrect to treat a missing rating as a rating of0during training?',
                'choices': [
                    ("Because missing usually means 'not observed', not 'disliked', and forcing zeros would bias the learned model.", True),
                    ('Because a rating of0is mathematically undefined in matrix multiplication.', False),
                    ('Because training requires all entries to be prime numbers.', False),
                    ('Because treating missing as0always improves accuracy, so it is avoided only for speed.', False),
                ]
            },
            {
                'text': 'Which of the following describes the update rule for a single step in Stochastic Gradient Descent?',
                'choices': [
                    ('θj:=θj−α(hθ(x(i))−y(i))xj(i)', True),
                    ('θj:=θj−α1m∑i=1m(hθ(x(i))−y(i))xj(i)', False),
                    ('θj:=θj−α1b∑k=ii+b−1(hθ(x(k))−y(k))xj(k)', False),
                    ('θj:=θj+α(hθ(x(i))−y(i))xj(i)', False),
                ]
            },
            {
                'text': 'Unlike Batch Gradient Descent, the path taken by Stochastic Gradient Descent toward the minimum usually:',
                'choices': [
                    ('Follows a perfectly straight line to the global optimum.', False),
                    ("Oscillates or 'wanders' around the minimum without necessarily settling at the exact point.", True),
                    ('Always approaches the minimum from the same direction.', False),
                    ('Takes much longer per individual parameter update step.', False),
                ]
            },
            {
                'text': 'According to theReward Hypothesis, all goals in an RL problem can be described as the maximization of which mathematical expression?',
                'choices': [
                    ('The expected cumulative rewardmaxE[∑i=0∞Rk+i+1]', True),
                    ('The immediate scalar realizationrk', False),
                    ('The constant discount rateγ', False),
                    ('The difference between action valuesqπand state valuesvπ', False),
                ]
            },
            {
                'text': 'Which of the following is a common cause ofTraining-Serving Skewin machine learning systems?',
                'choices': [
                    ('Using Nested Cross-Validation instead of simple K-fold [cite: 941]', False),
                    ('Fixed random seeds in the training pipeline [cite: 1013]', False),
                    ('Inconsistent preprocessing or transformation logic between training and inference [cite: 1059, 1061]', True),
                    ('Periodic retraining of the model on a weekly cadence [cite: 1134]', False),
                ]
            },
            {
                'text': 'What is the difference between theState-Value functionvπ(xk)and theAction-Value functionqπ(xk,uk)?',
                'choices': [
                    ('vπrepresents the actual reward, whileqπrepresents the estimated reward.', False),
                    ('vπis used only for episodic tasks, whileqπis used for continuing tasks.', False),
                    ('qπevaluates the expected return of taking a specific actionukin statexk, whilevπevaluates the state itself under policyπ.', True),
                    ('There is no difference; they are two names for the same mathematical realization.', False),
                ]
            },
            {
                'text': 'What is the formula for estimating the varianceσj2for thej-th feature?',
                'choices': [
                    ('σj2=1m∑i=1m(xj(i)−μj)2', True),
                    ('σj2=1m∑i=1m(xj(i)+μj)2', False),
                    ('σj2=m∑i=1m(xj(i)−μj)2', False),
                    ('σj2=1m∑i=1mxj(i)−μj', False),
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
