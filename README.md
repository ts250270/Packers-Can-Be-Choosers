# Packers-Can-Be-Choosers

CreateModel.py: in this script we create the word2vec model.
LoadModel.py: in this script we load the model and use it to create item clusters.
CreateBasketFile.py: in this script we create a file with many baskets to go over later and score.
BasketGradeCalculator.py: in this script we go over baskets and score each one, using the training set.
BasketGradeCalculator_ScoreByTestSet20.py: this script is similar to the previous but it uses the test set and also gives more details about the scoring.
Transactions.py: was used initially for db interaction but eventually not used.
