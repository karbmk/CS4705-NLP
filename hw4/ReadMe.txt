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
    To train, Run:
      python q5.py tag_train.dat suffix_tagger.model
    Then to tag, run:
      python q4.py suffix_tagger.model tag_dev.dat tag_dev_q5.out
    To evaluate the performance run:
      python eval_tagger.py tag_dev.key tag_dev_q5.out
  Part 2:
    Of the 2459 words to tag, the newly model got 2265 correct, for an accuracty of ~ 92 %.
    Output from eval_tagger.py:
      2265 2459 0.921106140708
  Part 3:
    The result of this model is around 92% correct. This is ~2% improvement from Q4, where 39 more tags were correctly determined. Clearly this helped the output, although the change wasn't HUGE.

Question 6

  Part 1:
    To train all features combinations, run:
      python q6.py tag_train.dat prefix_tagger.model prefix
      python q6.py tag_train.dat presuf_tagger.model presuf
      python q6.py tag_train.dat case_tagger.model case
      python q6.py tag_train.dat length_tagger.model len
    Then to tag all features combinations, run:
      python q4.py prefix_tagger.model tag_dev.dat tag_dev_pre.out
      python q4.py presuf_tagger.model tag_dev.dat tag_dev_ps.out
      python q4.py case_tagger.model   tag_dev.dat tag_dev_case.out
      python q4.py length_tagger.model tag_dev.dat tag_dev_len.out
    To evaluate the performances run:
      python eval_tagger.py tag_dev.key tag_dev_pre.out
      python eval_tagger.py tag_dev.key tag_dev_ps.out
      python eval_tagger.py tag_dev.key tag_dev_case.out
      python eval_tagger.py tag_dev.key tag_dev_len.out
  Part 2:
    Prefix Tagger Output from eval_tagger.py:
      2244 2459 0.912566083774
    Prefix and Suffix Tagger Output from eval_tagger.py:
      2262 2459 0.919886132574
    Case Tagger Output from eval_tagger.py:
      2242 2459 0.911752745018
    Length Tagger Output from eval_tagger.py:
      2208 2459 0.897925986173
  Part 3:
    The different features I ended up choosing are a Prefix tagger, a Prefix and Suffix Tagger, a Case Tagger, and a Lenght Tagger. The Prefix Tagger is just like the suffix tagger from Q5 except it looks for prefixes. It seemed like a natural extension of Q5. The Prefix and Suffix Tagger is a combination of those two. Next, the Case Tagger looks at lowercase/uppercase of the words, combined with numerical or punctuation information. There's also a tag for a mix in this model. Finally, I included a Length Tagger because I wanted to make sure I got credit for three, and I wasn't sure if the Prefix + Suffix Tagger would count.

    The Prefix, Prefix and Suffix, and Case Taggers all did better than the original model (Q4), but none did as well as the Suffix Tagger alone (Q5). I found this interesting because I included a Prefix and Suffix Tagger because Suffix and Prefix did so well separately, so I thought they would do even better together, but in actuality the Prefix brought the Suffix down, although the combination did do better than the Prefix alone. 

    The biggest failure is the Length Tagger, which did the worst among all the models explored in this assignment, although it's accuracy of 89.79% is not really that bad, just bad in comparison. Overall it seems the best I discovered was the Suffix Tagger, which was Q5. 
    
Question 7

  I didn't do it. 
