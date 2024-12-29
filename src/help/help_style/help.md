# Basic Ubuntu Commands

This is a list of the most basic but extremely useful commands. Learning these will help you have a strong foundation to add more sophisticated commands upon.

Here are some words that we use and some meanings that you may associate them with.

| We use    | What you may know them as |
| --------- | ------------------------: |
| directory |                    folder |
| sudo      |         Run as Administor |
| terminal  |                     Shell |
| prompt    |       active command line |
| echo      |                     print |

## Sudo

(Superuser DO) This is the same as "Run as administor"

```
user@my_computer_name:~$ sudo
```

## apt-get

[Link](https://google.com)

This command is used to install, update, upgrade, and remove any package. Examples below will show how to use in different ways:

- **sudo apt-get update**

  superuser privileges. This command updates your system along with the packages that are installed.

  ```
  user@my_computer_name:~$ sudo apt-get update
  ```

- **sudo apt-get upgrade**

  You will run this command after you ran

  ```
  user@my_computer_name:~$ sudo apt-get upgrade
  ```

  This will upgrade the packages that have available updates. You can also upgrade just one package by adding a space along with the package name after upgrade.

  ```
  user@my_computer_name:~$ sudo apt-get upgrade node.js
  ```

- **sudo apt-get install _package name you wish to install_**
  You would replace the package-name with the name of the program you wish to install.

  ```
  user@my_computer_name:~$ sudo apt-get install curl
  ```

## echo

echo is that useful of a command but we are going to use it to help us learn about command line arguments. In the example below each word in the command line is an argument.

```
user@my_computer_name:~$ echo Each word I enter in the command line is an argument.
Each word I enter in the command line is an argument.
```

But if we wrap " " or ' ' around the sentence then that sentence would be just one argument. Example:

```
user@my_computer_name:~$ echo "This sentence is only one argument"
This sentence is only one argument
```

The quotes " " or ' ' are ignored by the terminal (shell) but the sentence is counted as just one argument. This is good to learn because if we have a file or directory with spaces in it's name and we want to use that file or directory. We will have to use quotes " " or ' ' to tell the terminal to use it. If we did not and we try to use a command cat to see the content of a file and the file has spaces in it's name. The command would throw an error. So, in order to not throw an error we use quotes to make the file or directory as one argument. Example:

```
user@my_computer_name:~$ cat "my python program.py"
```

This would return the content in that file.

## ls

(list) command will list out the files in the current working directory you are in.

```
user@my_computer_name:~$ ls
Desktop  Documents  Webdev  Dev
```

You can also look at different files in other directories by adding a space then the direct path to the other directory you wish to look into.

```
user@my_computer_name:~$ ls Dev
Python  JS  HTML  CSS
```

We can also see hidden files by using the -a

```
user@my_computer_name:~/Dev$ ls -a
.I_was_hiding  Python  JS  HTML  CSS  .hidden.txt
```

This command will list all the files in that directory including hidden files.

- **ls -t**

This list command will return the directories or files in their time stamp order. This ls -t command can also be combined with -a. This combination would return a list of the hidden directories or files in their time stamp order. Example:

```
user@my_computer_name:~/Dev$ ls -a -t
HTML  CSS  JS  .hidden.txt  Python  .I_was_hiding
```

## whoami

(who am i) This command will return the username.

```
user@my_computer_name:~$ whoami
user
```

## cd

(change directory) used to change the current working directory. You use it by typing cd space then the file name within your current directory or full path to another directory and/or file if in a different directory. Examples of different ways below:

- cd /

```
user@my_computer_name:~Dev/Python$ cd /
user@my_computer_name:/$
```

- This will take me to the root directory. **Note that the ~ tilde is not in the return command line.**

- cd ..

```
user@my_computer_name:~/Dev/JS Practice$ cd ..
user@my_computer_name:~/Dev$
```

- This will take me from the JS Practice to it's parent directory Dev. **Note that JS Practice has a space. This is not a proper way to name a file**

  - In the example above: When I am in the Dev directory and want to access the file JS Practice I can do this two ways:

    1. `user@my_computer_name:~/Dev$ cd "JS Practice"`
    2. `user@my_computer_name:~/Dev$ cd JS\ Practice`

  - Both command lines would produce the same results. They would have cd (changed directory) in to JS Practice. **But try not to name files with spaces in them. Use an \_ underscore instead of a space.**

- cd -

```
user@my_computer_name:~/Dev$ cd -
user@my_computer_name:~/Dev/JS Practice$
```

- This took me to my previous directory from my History.

- cd ~

```
user@my_computer_name:~/Dev/JS Practice$ cd ~
user@my_computer_name:~$
```

- This took me to the user directory.

- This symbol ~ is called a tilde. This refers to your user directory.

## Relative and Absolute Paths

We used cd to change directory but in the examples above we used their relative path. Meaning the path we went to was relative to the parent directory. While using absolute paths, we start from the root directory and go down to the location you want to go. Examples below:

- Relative Path

```
user@my_computer_name:~$ ls
Desktop  Documents  Dev  Webdev
user@my_computer_name:~$ cd Dev/PracticePython
user@my_computer_name:~/Dev/PracticePython$
```

- Absolute Path

```
user@my_computer_name:~$ ls /
bin  dev  sys  home
user@my_computer_name:~/home$ ls
user
user@my_computer_name:~$ cd /home/user/Dev/PracticePython
user@my_computer_name:~/Dev/PracticePython$
```

## pwd

(print working directory) This will display the full pathname of the working directory.

Using the last example above -

```
user@my_computer_name:~Dev/Python/Practice$ pwd
/home/user/Dev/Python/Practice
```

## cp

(copy) - After typing cp you type the file you want to copy + space + location you want to place the copied file.

```
user@my_computer_name:~/Dev/Webdev$ cp app.js home/user/Dev/JS
If there is no error, means it worked
```

## mv

(move) A lot like cp (copy) but instead of copying the file you will move it from one directory to another directory. Just like cp (copy) after typing mv + space + the file you want to move + location to move it too. Example below:

```
user@my_computer_name:~/Dev/Python$ mv pyproject.py /home/user/Dev/Python/Project
If there is no error, means it worked
```

- This will move the pyproject.py file in my current directory to the Python_Project directory. You can also move directories using this command.

## rm

(remove) This command will remove the specified file but not the directory.

```
user@my_computer_name:~/Dev/Webdev$ rm myApp.js
If there is no error, means it worked
```

Here are some other uses of the rm command:

- **rmdir**

  (remove directory) - Removes an empty directory

```
user@my_computer_name:~/Dev$ rmdir My_Empty_Dir
If there is no error, means it worked
```

- **rm -r**

(remove recursively) - Removes a directory along with its content. This will remove a non-empty directory

```
user@my_computer_name:~/Dev$ rm -r No_Longer_Needed_Practice_File
If there is no error, means it worked
```

- **rm -f**

(remove force)
This will forcefully remove files.
But to forcefully remove non-empty dirctories use:

```
user@my_computer_name:~/Dev/Python$ rm -rf Non_Empty_Dir
If there is no error, means it worked
```

- **rm -i**

Using this will make rm prompt you before every removal.

```
user@my_computer_name:~/Dev/Python/Practice$ rm -i basic.py
rm: remove regular file? <You enter y(yes) or n(no) then press enter>
```

## mkdir

(make directory) This command will allow you to create a new directory. You can also specify where you want to create this directory's location by putting a space followed by the location behind mkdir. Example:

```
user@my_computer_name:~$ mkdir Basic_Terminal /home/user/Dev/Bash
If there is no error, means it worked
```

Or if I wish to make a new directory in the current directory I would do:

```
user@my_computer_name:~/Dev/Bash$ mkdir Learn_Terminal_Basic
If there is no error, means it worked
```

## To Make File

To make a file in your current directory do:

```
user@my_computer_name:~/Dev/Bash$ nano file_name_you_want
```

This will open up the nano program, built into Terminal, with the file_name_you_want. (More on nano is explained below)

## ctrl+c

control + c Now that we are dealing with more argument commands we need to learn how to break out of them. If you are in a command argument and for some reason you want to break out of it. You would use ctrl+c

```
user@my_comuter_name:~$ if [Dev]; then echo "There is a Dev directory" else echo "There is not a Dev directory" <you hit the enter key but forgot the closing fi>
>  <but the command line is still waiting for more input. So, you hit enter again>
> <and again because you forgot how to end and want to start over>
>
> <You can cancel the conditional statement by> ctrl+C
^C
user@my_computer_name:~$
```

As we can see from the command line that went we used the ctrl+c that the terminal displays ^C. This is normal. That is the output of our command ctrl+c. As you will see when using the command that it breaks you out of the argument or conditional statement in our example and returns your active command line back, ready for you to enter any new commands.

## locate

Use this command to find files and their location by their name. If you are not sure if the file name is upper case or lower case use -i to ignore the case.
If you wish to locate two or more words at a time you can seprate each word with (\*). Example below:

```
user@my_computer_name:~$ locate -i *hello*Practice
/home/user/Dev/JS
/home/user/Dev/Python
/home/user/Dev/Bash
<And all other locations where hello or Hello and practice or Practice is located from the root directory to the last dir in the tree directory>
```

If you just want to have a count of the times the word is in the directories you can use -c. Example:

```
user@my_computer_name:~$ locate -c Python
6062
```

This would return a number of how many times the word Python is in the directories.

or you could do this:

```
user@my_computer_name:~$ locate -ic Python
92006
```

This will ignore the case and return a count for how many times Python and/or python is in the directories.

## find

This command will search the current directory and sub-directories. You can also use the wild card command with the option -name to find extentions. Example below.

```
user@my_computer_name:~$ find Dev
Dev
```

```
user@my_computer_name:~/Dev/Python$ find -name "*.py"
./hello.py
./test.py
./play.py
```

## history

This command will display all of your previous commands **up to the history memory limit.**

```
user@my_computer_name:~\$ history
1 cd ~
2 top
3 man top
and so on...
```

## df

(display filesystem) This will display information about your disk space usage of your filesystem.

```
user@my_computer_name:~\$ df
Filesystem 1K-blocks Used Available Use% Mounted on
udev 5846980 0 5846980 0% /dev
tmpfs 1180420 2072 1178348 1% /run
/dev/sda5 479122128 33007000 421707372 8% /
and so on...
```

df can aslo be told to display a more reader friendly content.

```
user@my_computer_name:~\$ df -h
Filesystem Size Used Avail Use% Mounted on
udev 5.6G 0 5.6G 0% /dev
tmpfs 1.2G 2.1M 1.2G 1% /run
/dev/sda5 457G 32G 403G 8% /
and so on...
```

## free

This command displays the amount of free space available on the system.

```
user@my_computer_name:~\$ free
total used free shared buff/cache available
Mem: 11804196 2661544 7855232 56584 1287420 8985272
Swap: 2097148 0 2097148
```

free can also be told to display a more reader friendly content.

```
user@my_computer_name:~\$ free -h
total used free shared buff/cache available
Mem: 11G 2.5G 7.5G 55M 1.2G 8.6G
Swap: 2.0G 0B 2.0G
```

## top

This will display the processes using the most resources. You can exit out by typing q

```
user@my_computer_name:~\$ top
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
2298 user 20 0 684664 124244 95140 S 31.5 1.1 12:35.16 chrome
2632 user 20 0 1009140 245928 100964 R 31.5 2.1 15:01.70 chrome
and so on ...
q
```

This is just a small example of the power of top. To get a full understanding of top I suggest using `info top`

## cat

Displays the contents of a file. We saw an example of this at the begining of this cheatsheet.

```
user@my_computer_name:~\$ cat Dev/Practice/basic.py
def helloWorld():
print("Hello World!")
```

or to cat in your current directory

```
user@my_computer_name:~/Dev/Python\$ cat basic.py
def helloWorld():
print("Hello World!")
```

We can also have cat return our content with number line printout. We can do this by using the -n with our cat command. Example:

```
user@my_computer_name:~ /Dev/Python\$ cat -n basic.py

1. def helloWorld():
2. print("Hello World!")
```

## less

This command is like the cat command but the differents is that cat will display all your content at once while less shows you the top of the file that will fill the terminal screen and you can use the space bar to move down line by line or use the down arrow. less also lets you move back up with the up arrow. And when you reach the bottom of the content, less will not quite the command which lets you move back up if you want. But if you are done you must press q to quit out of less. Unlike cat less will remove the content and allows you to see your previous command lines. Which I like because it seems less cluttery.

To save space I will not show example that will fill the full screen.

```
user@my_computer_name:~/Dev/Python\$ less hello.py

# When ran the print out will say Hello <your name>

first_name = input("What is your name? ")
print("Hello,", first_name)
if first_name == "Matt":
print(first_name, "is learning Python")
elif first_name == "Maximiliane":
print(first_name, "is learning with fellow students in the community! Me too!")
else: .... and so on
...
END
q
```

Long example but I think you get the picture of how the command less works. When you have ended the content, END will be printed. You can excape from the less command by pressing q.

## man

(manual) This command will give you a description of any command that come after the command man. Example:

```
user@my_computer_name:~\$ man install
INSTALL(1) User Commands INSTALL(1)

NAME
install - copy files and set attributes

SYNOPSIS
install [OPTION]... [-T] SOURCE DEST
install [OPTION]... SOURCE... DIRECTORY
install [OPTION]... -t DIRECTORY SOURCE...
install [OPTION]... -d DIRECTORY...
...
```

This is just some of the content that man install returned.

## info

(information) This command is a lot like man but the different is that info goes into more information about the command. Example:

```
user@my_computer_name:~\$ info apt-get
APT-GET(8) APT APT-GET(8)

NAME
apt-get - APT package handling utility -- command-line interface

SYNOPSIS
apt-get [-asqdyfmubV][-o=config_string] [-c=config_file][-t=target_release] [-a=architecture] {update | upgrade |
dselect-upgrade | dist-upgrade |
...
```

This is just some of the content that info apt-get returned.

## rename file or directory

Ubuntu 18.04 does not have the command rename installed but can be installed using:

```
user@my_computer_name:~\$ sudo install rename
```

But the Ubuntu community recommands using mv command. Let's say I have a file in my Dev directory I want to rename.

```
user@my_computer_name:~\$ mv /home/user/Dev/Basic_Terminal_Commands/basic_commands.md /home/user/Dev/Basic_Terminal_Commands/ubuntu_terminal_commands.md
If there is no error, means it worked
```

Here is another way that was suggested but it is more complicated:

```
user@my_computer_name:~$ for file in <the file or dir you want to rename>; do mv $file \${file//<name of the file or dir you want to rename>/<the new name you want>}; done
If there is no error, means it worked
```

## clear

clear will clear everything off your terminal display except your active directory/file command line.

```
user@my_computer_name:~\$ clear
```

## Ctrl+l

This command is the same as clear command but it just a shortcut command.

# Built in editors in Unix Systems

## Nano

In most Unix systems they have an user friendly editor program called nano. Nano is very straight forward to write in. To use the editor use the command nano. See example below

```
user@my_computer_name:~/Dev/Python$ nano play_in_python.py
  GNU nano 2.9.3                       test.py                        Modified

# I am learning new ways to use my command line skills.

def hello():
        print("Hello Command line")
















^G Get Help  ^O Write Out ^W Where Is  ^K Cut Text  ^J Justify   ^C Cur Pos
^X Exit      ^R Read File ^\ Replace   ^U Uncut Text^T To Linter ^_ Go To Line
```

As we see in this example. In order to save our info in the editor we must use the Ctrl(Control key) plus O and Ctrl+X to Exit nano.

## Vim or older version Vi

## Ubuntu Terminal Shortcuts

| Shortcuts                          |                                                                                                        Functions |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------: |
| Ctrl + Shift + T                   |                                                                              Open new tab on the active terminal |
| Ctrl + Shift + W                   |                                                                                             Close the active tab |
| Ctrl + A                           |                                                                      Move cursor to beginning of the active line |
| Ctrl + E                           |                                                                            Move cursor to end of the active line |
| Ctrl + U                           |                                                                                    Clears the entire active line |
| Ctrl + K                           |                                                                  Clears the command from the cursor to the right |
| Ctrl + W                           |                                                                                Delete the word before the cursor |
| Ctrl + R                           |                                                   Searches your history for commands matching what you had typed |
| Ctrl + C                           |                                                                                          Kill the active process |
| Ctrl + Z                           |                                               Temporarily stops the active process by sending the signal SIGSTOP |
| Ctrl + L                           |                                                                                      Clears the terminal display |
| Alt + F                            |                                                                                        Advances forward one word |
| Alt + B                            |                                                                                               Goes back one word |
| Ctrl + Shift + C                   |                                                                 Copy the highlighted characters to the clipboard |
| Ctrl + Shift + V or Shift + Insert |                                                           Paste the contents of the clipboard to the active line |
| Up/Down Arrow Keys                 | Scrolls through your command history, This can allow you to quickly execute your previous command multiple times |
| TAB                                |                 Can complete the command you are typing. Can also be use to complete mulitple commands in a row. |

