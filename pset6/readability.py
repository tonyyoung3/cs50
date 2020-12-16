import cs50 as cs

word = 1;
sentence = 0;
letter = 0;
Grade = 0;



text = cs.get_string("Text : ")
for i in range(len(text)):
    if text[i] == ' ':
      word +=1;
    if text[i].isalpha() == True:
      letter +=1;
    if text[i] == '!' or text[i] == '.' or text[i] == '?':
      sentence +=1;

    Grade = round(0.0588 * (letter / word) * 100 - 0.296 * (sentence / word) * 100 - 15.8);

if Grade < 1:
  print("Before Grade 1 ")
elif Grade >= 16:
  print("Grade 16+")
else:
  print("Grade " + str(Grade))
