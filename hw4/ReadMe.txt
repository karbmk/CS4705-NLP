Emily Schultz (ess2183)
COMS 4705 - Natural Language Processing
Due: 12/6/13, 5PM

Homework 4 Programming Assignment

Question 4

  Part 1:
    Run:
      python q4.py tag.model tag_dev.dat tag_dev.out
    To evaluate the performance run:
      python eval_tagger.py tag_dev.key tag_dev.out
  Part 2:
    Of the 2459 words to tag, my program got 2226 correct, for an accuracy of ~ 90.5 %.
    Output from eval_tagger.py:
      2226 2459 0.905246034974
  Part 3:
    The result of this model is around 90% correct, which is fairly accurate.

Question 5

  Part 1:
    Run:
      python q5.py tag_train.dat q5.model
    Then run:
      python q4.py q5.model tag_dev.dat tag_dev_q5.out
    To evaluate the performance run:
      python eval_tagger.py tag_dev.key tag_dev_q5.out
  Part 2:
    Of the 2459 words to tag, the newly model got 2265 correct, for an accuracty of ~ 92 %.
    Output from eval_tagger.py:
      2265 2459 0.921106140708
  Part 3:
    The result of this model is around 92% correct. This is ~2% improvement from Q4, where 39 more tags were correctly determined.
  Part 4:

Question 6

  Part 1:
  Part 2:
  Part 3:
  Part 4:

Question 7
  I totally didn't do it. 
