NAIVE BAYES SPAM FILTERING

1. Two sets of messages are suupplied to the algorithm (spam and non-spam). These can be obtained from extensively researched datasets like Enron dataset.

2. In both sets, each message is reduced to a 'bag of words', keeping individual words from the message ignoring any syntactical structure or order of original message.

3. For all words in both sets, each word's spamicity is calculated. 
   Spamicity of a word is the probability that a message containing that word should be considered spam.
  
4. Once the training process is completed (by caculatuing spamicities of all words across spam and ham sections of the dataset), the classifier can be put to use.
   For each new e-mail, product of the spamicities of all words present in the incoming e-mail is used to calculate spam probability of the e-mail.


Steps 3 and 4 make use of equations provided under Bayes' Theorem.

INTERACTIVE UI (basic)

1. Spam and ham e-mails have been segregated. We now ignore the spam e-mails.

2. Non-spam e-mails are sorted by their timestamp (latest ones must appear at the top).

3. Only the titles of these e-mails are displayed  to the user.

4. The user may enter index/part-title of a particular e-mail to read the whole of it.
