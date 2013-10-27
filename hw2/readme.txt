Emily Schultz (ess2183@columbia.edu)
NLP: COMS 4705
Homework 2: Programming Problems (Q4,Q5,Q6)

* Sorry this was one day late *

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
    This takes about a minute.

  Part 2:
    If you wish, you can run:
      python pretty_print_tree.py parse_train_rare.dat
    to see the tree produced and check if the file is in the proper format.
    The script does not throw an error, so the tree is in the proper format. That's good.

  Part 3: 
    None.

  Part 4:
    None.


Question 5:
  Write rule parameters q and implement the CKY algorithm.

  Part 1:
    First run all parts from  Question 4 (above).
    Then run:
      python cky.py parse_dev.dat cfg_rare.counts > cky_output
    to produce the cky_output file containing the results from the CKY Algorithm.
    This will take several minutes (max 10 min). You can see the sentence it's working on in the terminal (or you can comment out line 149).
    Then run:
      python eval_parser.py parse_dev.key cky_output
    to see how well the parser did (results below).

  Part 2:
    Output from eval_parser.py:

          Type       Total   Precision      Recall     F1 Score
    ===============================================================
             .         370     1.000        1.000        1.000
           ADJ         164     0.827        0.555        0.664
          ADJP          29     0.333        0.241        0.280
      ADJP+ADJ          22     0.542        0.591        0.565
           ADP         204     0.955        0.946        0.951
           ADV          64     0.694        0.531        0.602
          ADVP          30     0.333        0.133        0.190
      ADVP+ADV          53     0.756        0.642        0.694
          CONJ          53     1.000        1.000        1.000
           DET         167     0.988        0.976        0.982
          NOUN         671     0.752        0.842        0.795
            NP         884     0.626        0.525        0.571
        NP+ADJ           2     0.286        1.000        0.444
        NP+DET          21     0.783        0.857        0.818
       NP+NOUN         131     0.641        0.573        0.605
        NP+NUM          13     0.214        0.231        0.222
       NP+PRON          50     0.980        0.980        0.980
         NP+QP          11     0.667        0.182        0.286
           NUM          93     0.984        0.645        0.779
            PP         208     0.597        0.635        0.615
          PRON          14     1.000        0.929        0.963
           PRT          45     0.957        0.978        0.967
       PRT+PRT           2     0.400        1.000        0.571
            QP          26     0.647        0.423        0.512
             S         587     0.626        0.782        0.695
          SBAR          25     0.091        0.040        0.056
          VERB         283     0.683        0.799        0.736
            VP         399     0.559        0.594        0.576
       VP+VERB          15     0.250        0.267        0.258

         total        4664     0.714        0.714        0.714

  Part 3:
    As you can see from the above table, the results were fairly good. Of the 4664 total words, the algorithm had an overall precision and recall of 0.714, giving it an F1-score of 0.714 as well. It did perfectly on punctuation '.' and conjunctions, and had perfect precision on pronouns. It also did very well with adp, determiner, noun phrase + determiner, noun phrase + pronoun, and prt rules. The algorithm seemed to struggle with adjp, adverb phrase, noun phrase + numeral, and verb phrase + verb rules. This makes sense because words fitting these rules often are associated with a lot of ambiguity. It seems to often label a NOUN as a VERB+VERBP, especially for _RARE_ words. Hopefully the vertical markovization for Question 6 will improve these results. 

  Part 4:
    None.

Question 6:
  Introduce Vertical Markovization into CKY Algorithm.

  Part 1:

    First, from Q4, run:
      python count_cfg_freq.py parse_train_vert.dat > cfg_vert.counts
    to produce the initial counts of the rules used in the corpus.
    Now run:
      python p4.py cfg_vert.counts parse_train_vert.dat > parse_train_vert_rare.dat
    to produce the new training file (~1 min)
    and 
      python count_cfg_freq.py parse_train_vert_rare.dat > cfg_rare_vert.counts
    to produce the counts of the rules used in the corpus with the _RARE_ keyword.

    Run:
      python cky.py parse_dev.dat cfg_rare_vert.counts > cky_vm_output
    to produce the cky_vm_output file containing the results from the CKY Algorithm with Vertical Markovization.
    This will take several minutes (~ 20 min or 5s/sentence). You can see the sentence it's working on in the terminal (or you can comment out line 149).

    Then run:
      python eval_parser.py parse_dev.key cky_vm_output
    to see how well the parser did (results below).

  Part 2:
          Type       Total   Precision      Recall     F1 Score
    ===============================================================
             .         370     1.000        1.000        1.000
           ADJ         164     0.689        0.622        0.654
          ADJP          29     0.324        0.414        0.364
      ADJP+ADJ          22     0.591        0.591        0.591
           ADP         204     0.960        0.951        0.956
           ADV          64     0.759        0.641        0.695
          ADVP          30     0.417        0.167        0.238
      ADVP+ADV          53     0.700        0.660        0.680
          CONJ          53     1.000        1.000        1.000
           DET         167     0.988        0.994        0.991
          NOUN         671     0.796        0.851        0.823
            NP         884     0.618        0.550        0.582
        NP+ADJ           2     0.333        0.500        0.400
        NP+DET          21     0.944        0.810        0.872
       NP+NOUN         131     0.610        0.656        0.632
        NP+NUM          13     0.375        0.231        0.286
       NP+PRON          50     0.980        0.980        0.980
         NP+QP          11     0.750        0.273        0.400
           NUM          93     0.970        0.688        0.805
            PP         208     0.623        0.635        0.629
          PRON          14     1.000        0.929        0.963
           PRT          45     1.000        0.933        0.966
       PRT+PRT           2     0.286        1.000        0.444
            QP          26     0.722        0.500        0.591
             S         587     0.704        0.814        0.755
          SBAR          25     0.667        0.400        0.500
          VERB         283     0.790        0.813        0.801
            VP         399     0.663        0.677        0.670
       VP+VERB          15     0.294        0.333        0.312

         total        4664     0.743        0.743        0.743

  Part 3:
    Vertical Markovization did help the overall performance of the algorithm, which now has a Precision/Recall/F1 Score of 0.743 overall, compared to 0.714 from Q5.

    On average, most type improved a little bit in most categories, such as ADP, Nouns, and NP+Num. NP + DET had a significant increase in precision.
    The most significant increase was for SBAR, which went from a horrible precision of 0.091 to a solid 0.667 with vertical markovization. Recall also increased from 0.040 to 0.400, giving it an F1-Score of 0.500 rather than 0.051 from before. 
    Adjectives decreased significantly in terms of precision, but increased a little in recall. PRT+PRT dropped to nearly half of it's initial precision value, although it maintained the 1.000 recall value. The dismal ADVP from Q5 became slightly less dismal, especially in terms of precision. S decreased overall in all three categories, faring the worst from vertical markovization, although it's decreases are minor compared to the increases most made. 

  Part 4:
    The parser's output was improved on sentence 48: Short-term interest rates fell yesterday at the government 's weekly Treasury bill auction .
    The original CKY parser gave the tree:
      [S,
       [NP, [NOUN, Mrs.], [NOUN, _RARE_]],
       [S,
        [VP,
         [VERB, said],
         [NP,
          [NP+NOUN, yesterday],
          [PP, [ADP, that], [NP, [DET, the], [NOUN, _RARE_]]]]],
        [S,
         [NP, [NOUN, _RARE_], [NOUN, _RARE_]],
         [S,
          [NP+DET, this],
          [S,
           [VP, [VERB, _RARE_], [NP, [NOUN, government], [NOUN, _RARE_]]],
           [., .]]]]]]
    While Vertical Markovization CKY gave the tree:
      [S, [NP^<S>, [NOUN, Mrs.], [NOUN, _RARE_]], [S,
        [VP^<S>,
         [VERB, said],
         [VP,
          [NP^<VP>+NOUN, yesterday],
          [SBAR^<VP>,
           [ADP, that],
           [S^<SBAR>,
            [NP^<S>, [DET, the], [NOUN, _RARE_]],
            [VP^<S>,
             [VERB, _RARE_],
             [VP^<VP>,
              [VERB, _RARE_],
              [NP^<VP>,
               [DET, this],
               [NP,
                [NOUN, _RARE_],
                [NP, [NOUN, government], [NOUN, _RARE_]]]]]]]]]],
        [., .]]]    
    And the correct tree is:
      [S,
       [NP, [NOUN, Mrs.], [NOUN, Hills]],
       [S,
        [VP,
         [VERB, said],
         [VP,
          [NP+NOUN, yesterday],
          [SBAR,
           [ADP, that],
           [S,
            [NP, [DET, the], [NP, [ADJ, dispute-settlement], [NOUN, panel]]],
            [VP,
             [VERB, rejected],
             [NP,
              [DET, this],
              [NP,
               [ADJ, Canadian],
               [NP, [NOUN, government], [NOUN, argument]]]]]]]]],
        [., .]]]    
    Clearly the Vertical Markovization more accurately determined the structure of the tree, and identified the SBAR that the initial CKY did not. 
