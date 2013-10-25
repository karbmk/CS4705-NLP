Emily Schultz (ess2183@columbia.edu)
NLP: COMS 4705
Homework 2: Programming Problems (Q4,Q5,Q6)


Question 4:
  Replace infrequent words (Count(x) < 5) in the original training data file with a common symbol _RARE_.

  Part 1:
    First run:
      python count_cfg_freq.py parse_train.dat > cfg.counts
    to produce the initial counts of the rules used in the corpus.

    Now run:
      python p4.py cfg.counts parse_train.dat > parse_train_rare.dat
    to produce the new training file
    and 
      python count_cfg_freq.py parse_train_rare.dat > cfg_rare.counts
    to produce the counts of the rules used in the corpus with the _RARE_ keyword.

  Part 2:
    If you wish, you can run:
      python pretty_print_tree.py parse_train_rare.dat
    to see if the file is in the proper format.
    The script does not throw an error, so the tree is in the proper format. That's good.

  Part 3: 
    None.

  Part 4:
    None.

Question 5:

  Part 1:
  Part 2:
  Part 3:
  Part 4:

Question 6

  Part 1:
  Part 2:
  Part 3:
  Part 4:
