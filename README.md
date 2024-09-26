# Basic Crypto Converter
## Video Demo: unlisted
## Description:
The program is a basic crypto to euro converter with a colourful yet simple graphical user interface. After testing a few concepts, I decided to expand on an idea that I had while working on one of the problem sets for this course, namely, the Bitcoin Price Index. My program retrieves up-to-date prices via the Binance API. Initially, I wanted to be able to convert from a number of fiat currencies to various different cryptos but, due to time and technical restraints, I decided to focus on a single currency, the Euro, and a handful of cryptos (BTC, BCH, ETH, LTC). (I'm sure that as time goes by I will continue to tinker with and update the program!)

### Technical Details
To implement the GUI, I used Tkinter, as it seemed to be one of the most popular libraries and therefore has a wealth of documentation and tutorial content. It also appeared to be one of the most straightforward ways of implementing a GUI for a small project like this.

To use the "modern" features, I imported both the classic and new widgets (along with some other features), like so:
```
from tkinter import *
from tkinter import ttk, messagebox, PhotoImage
```
The other libraries that were required are "re" for regular expressions, and "requests", to access the latest prices via the Binance API.

#### Functionality
The program consists of a basic GUI, arranged using the Tkinter grid system. In a fixed-size window we find a dropdown menu, a number of text labels, entry fields for crypto and fiat amounts and 2 buttons; one to convert and the other to clear all fields.

The dropdown menu allows you to choose the crypto you would like to convert. Choosing a crypto updates the corresponding text label below so that it displays the selection (this is also shown in the dropdown too). Should you not specify a crypto and try to use the convert button, the program will prompt you to make a selection first, via a pop-up window, or "messagebox":

`"no_crypto": lambda: messagebox.showerror(message="Please select a cryptocurrency!"`

You can then enter a number in either of the fiat or crypto fields and hit convert.
Should any input not be valid, another messagebox will pop up telling you what the issue is (for example, if you've written "cat" instead of a number, it'll ask you to enter a valid number).

There is also a clear button to allow you delete all entries and start another conversion.

The process to convert goes as follows:

- Clicking the "Convert" button will call the click_convert function, which passes the input from the entry fields to main.
- The main function takes care of passing the input to several functions. First, it passes it to the input_check function which will determine how to handle the input or notify of an error, should the input not be valid.
- If the input is valid, input_check will pass it to the corresponding conversion function, depending on the 'direction' of the conversion. For a crypto to fiat conversion, input_check passes the input, c, to the crypto2fiat function. For the opposite conversion, main passes the input, f, to fiat2crypto.
- At the same time, input_check passes back an instruction to main so that it can implement the corresponding GUI update via the update_GUI functions. Each entry field is automatically updated with the result as a fully formatted number, regardless of how it was entered, e.g., entering "1500.50" in euros will come back as "€1,500.50":
`update_fiat = f"€{float(f):,.2f}"`
- The conversion functions take the up-to-date price from the Binance API via the crypto_price function to do the calculation. More info on this API here: https://binance-docs.github.io/apidocs/spot/en/#general-info
- There are a few other functions that are used to clean up user input and check that it can be converted to a float.

The rest of the program deals with the GUI setup. After getting to grips with the syntax, I was able to implement several features from Tkinter such as coloured backgrounds, images, replacing text and using buttons to trigger functions.

### Challenges
A lot of this code had to be re-written a few times. At first, I had a fully functioning program, but the logic was confused and confusing (:D) and difficult to test. Essentially, I had to re-think how I was passing the user input to each function.

Owing to the two-way nature of conversions, I had to separate *fiat to crypto* from *crypto to fiat*, for both number crunching and GUI updates.

Some other challenges that I faced:
- Keeping track of functions and variables! Since this was a far larger project than anything I had worked on before, it was important to be able to easily follow the logic.
- Structure is also important so, after getting most of the code down, I took some time to arrange it sensibly without breaking functionality. The first half is for the logic, the second deals with the GUI.
- This was my first experience designing and writing for a GUI. Fortunately the Tkinter library is relatively easy to get to grips with, although I couldn't seem to completely figure out some of the grid positioning which led me to disabling window resizing!
- Entry field tracking. I would have liked to have the entry fields dynamically detect any new input and allow you to convert again without having to clear all first. However, despite numerous attempts, I could not figure out how to do this without causing issues elsewhere in the program.

#### Testing
Since the program utilises tkinter, I ran into a few issues when writing tests for it. After a bit of research and some help from the ddb, I managed to figure out how to use 'patch' from unittest.mock to ensure functions that depended on certain tkinter features could still be tested:
```
def test_crypto2fiat():
    with patch("project.crypto_price", return_value=100) as mock_get:
        assert crypto2fiat("2") == 200
        assert crypto2fiat("0.5") == 50
```
```
def test_input_check():
    with patch("project.crypto_menu.get", return_value="BTC") as mock_get:
        assert input_check("", "") == "empty"
        assert input_check("10", "") == "c2f"
        assert input_check("", "10") == "f2c"
```

#### Improvements
I'm sure that there are plenty of lines of code in this program that could be cleaned up and made more succinct. However, since I have broken and fixed this program several times already, I will try to get some more experience under my belt before attempting that!

As mentioned earlier, the functionality of the program can be greatly expanded. In particular, the dynamic entry fields are something that I really want to figure out!

I found that I still had some reliance on the duck debugger for the more complex parts of code, and I'd like to develop more autonomy.