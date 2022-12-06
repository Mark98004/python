from random import randint

num = randint(1, 100);
print(num)

while 1:
  ans = int(input("Please enter a number:"));
  if ans == num:
    print("You win!");
    break;
  elif ans > num:
    print("Too big");
  else:
    print("Too small");