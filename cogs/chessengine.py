from discord.ext import commands

class ChessEngine(commands.Cog):
    @commands.group()
    async def chessengine(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("""
Hi. This is a simple guide to help you get started with writing your own chess engine. Every parts will be divided into subcommands.
I would like to call this a "wiki" because it will include some advanced topics as well, but if you just want to do this for fun, I also guided what to read next after each article.
There will be code examples for each part, so don't worry if you don't understand how to implement it in your engine. (but i know what are you gonna do heheheheh)

Note that this is written in Python, but the concept is kinda the same. Install the newest Python version at https://www.python.org/downloads/release/python-3135/

Type `>chessengine gettingstarted` for more info.
""")
            
    @chessengine.command(name="gettingstarted", help="Getting started with writing a chess engine")
    async def gettingstarted(self, ctx):
        await ctx.send("""
Writing a chess engine is a lot of work, but it can be a fun and rewarding project.
If you are new, you can start with a library. I will use the `python-chess` package here. https://python-chess.readthedocs.io for more info.
There are 3 main parts of a chess engine:
1. The board representation
2. The board evaluation
3. The search algorithm

So, let's start with the first part. Use `>chess engine boardrepresentation` to continue.
""")
    
    @chessengine.command(name="boardrepresentation", help="A brief documentation about board representation")
    async def boardrepresentation(self, ctx):
        await ctx.send("""
With `python-chess` it's quite easy to represent a chessboard. There is a built-in `Board` class with all the rules of chess and a `unicode()` method for displaying an Unicode board.
Here is an example about how to use it:
```py
import chess

board = chess.Board()
print(board.unicode(
    # These are the optional parameters you can use for your board
    invert_color=True, # Invert the color of the black pieces
    borders=False, # Shows borders around the board
    empty_square=".", # The character for empty squares
    orientation=chess.WHITE # The orientation of the board
))
```

Done reading? Nice. Let's continue with the second part - evaluation. Use `chessengine evaluation` to continue.          
""")
        
    @chessengine.command(name="evaluation", help="A brief documentation about board evaluation")
    async def evaluation(self, ctx):
        await ctx.send("""
**Evaluating** a chess position is a very complex task, but let's start with a simple evaluation function.
The most basic thing you can do is to count the material on the board. So first, we need to define the values of the pieces:
The unit we are using here is **centipawns**, which is 1/100 of a pawn. This is to avoid floating point calculations as much as possible and can make evaluating slightly faster.
We are also returning the evaluation in **White's perspective**, so if the evaluation is positive, means White is better.

Here is a pseudocode example on how to count material, no real code? please don't be a copycat
```
    def evaluate(board):
        PIECE_VALUES = {
            PAWN: 100,
            KNIGHT: 300,
            BISHOP: 300,
            ROOK: 500,
            QUEEN: 900,
            KING: 20000, # The king is invaluable so you can set it to any value
        }
                       
        white score = 0
        black score = 0
                       
        loop through all squares on the board:
            if square is empty:
                skip
            
            if piece color is white:
                white score += value of piece type at current square
            else:
                black score += value of piece type at current square
    ```
This is a very basic evaluation function, but it can be a good starting point. Alright, after you understand how this works, we can finally move on to the last part - the search algorithm. Use `>chessengine minimax` to continue.
""")
    @chessengine.command(name="minimax", help="A brief documentation about the minimax algorithm")
    async def minimax(self, ctx):
        await ctx.send("You can read about the explanation of minimax here: https://docs.google.com/document/d/1f6Xrm-6T2NAjBnnoDXRhdUJLl3NmTY_nEJXXtDP1Q4c/")
async def setup(bot):
    await bot.add_cog(ChessEngine(bot))