from __future__ import annotations
__author__='Niklas Fiekas'
__email__='niklas.fiekas@backscattering.de'
__version__='1.11.2'
import collections
import copy
import dataclasses
import enum
import math
import re
import itertools
import typing
from typing import ClassVar,Iterable,List,Literal,Optional,SupportsInt,TypeVar,Union
EnPassantSpec=Literal['legal','fen','xfen']
Color=bool
WHITE=True
BLACK=False
COLORS=[WHITE,BLACK]
ColorName=Literal['white','black']
COLOR_NAMES=['black','white']
PieceType=int
PAWN=1
KNIGHT=2
BISHOP=3
ROOK=4
QUEEN=5
KING=6
PIECE_TYPES=[PAWN,KNIGHT,BISHOP,ROOK,QUEEN,KING]
PIECE_SYMBOLS=[None,'p','n','b','r','q','k']
PIECE_NAMES=[None,'pawn','knight','bishop','rook','queen','king']
def piece_symbol(piece_type):return typing.cast(str,PIECE_SYMBOLS[piece_type])
def piece_name(piece_type):return typing.cast(str,PIECE_NAMES[piece_type])
FILE_NAMES=['a','b','c','d','e','f','g','h']
RANK_NAMES=['1','2','3','4','5','6','7','8']
STARTING_FEN='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
STARTING_BOARD_FEN='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
class Status(enum.IntFlag):VALID=0;NO_WHITE_KING=1<<0;NO_BLACK_KING=1<<1;TOO_MANY_KINGS=1<<2;TOO_MANY_WHITE_PAWNS=1<<3;TOO_MANY_BLACK_PAWNS=1<<4;PAWNS_ON_BACKRANK=1<<5;TOO_MANY_WHITE_PIECES=1<<6;TOO_MANY_BLACK_PIECES=1<<7;BAD_CASTLING_RIGHTS=1<<8;INVALID_EP_SQUARE=1<<9;OPPOSITE_CHECK=1<<10;EMPTY=1<<11;RACE_CHECK=1<<12;RACE_OVER=1<<13;RACE_MATERIAL=1<<14;TOO_MANY_CHECKERS=1<<15;IMPOSSIBLE_CHECK=1<<16
STATUS_VALID=Status.VALID
STATUS_NO_WHITE_KING=Status.NO_WHITE_KING
STATUS_NO_BLACK_KING=Status.NO_BLACK_KING
STATUS_TOO_MANY_KINGS=Status.TOO_MANY_KINGS
STATUS_TOO_MANY_WHITE_PAWNS=Status.TOO_MANY_WHITE_PAWNS
STATUS_TOO_MANY_BLACK_PAWNS=Status.TOO_MANY_BLACK_PAWNS
STATUS_PAWNS_ON_BACKRANK=Status.PAWNS_ON_BACKRANK
STATUS_TOO_MANY_WHITE_PIECES=Status.TOO_MANY_WHITE_PIECES
STATUS_TOO_MANY_BLACK_PIECES=Status.TOO_MANY_BLACK_PIECES
STATUS_BAD_CASTLING_RIGHTS=Status.BAD_CASTLING_RIGHTS
STATUS_INVALID_EP_SQUARE=Status.INVALID_EP_SQUARE
STATUS_OPPOSITE_CHECK=Status.OPPOSITE_CHECK
STATUS_EMPTY=Status.EMPTY
STATUS_RACE_CHECK=Status.RACE_CHECK
STATUS_RACE_OVER=Status.RACE_OVER
STATUS_RACE_MATERIAL=Status.RACE_MATERIAL
STATUS_TOO_MANY_CHECKERS=Status.TOO_MANY_CHECKERS
STATUS_IMPOSSIBLE_CHECK=Status.IMPOSSIBLE_CHECK
class Termination(enum.Enum):CHECKMATE=enum.auto();STALEMATE=enum.auto();INSUFFICIENT_MATERIAL=enum.auto();SEVENTYFIVE_MOVES=enum.auto();FIVEFOLD_REPETITION=enum.auto();FIFTY_MOVES=enum.auto();THREEFOLD_REPETITION=enum.auto();VARIANT_WIN=enum.auto();VARIANT_LOSS=enum.auto();VARIANT_DRAW=enum.auto()
@dataclasses.dataclass
class Outcome:
	termination:Termination;winner:Optional[Color]
	def result(self):return'1/2-1/2'if self.winner is None else'1-0'if self.winner else'0-1'
class InvalidMoveError(ValueError):pass
class IllegalMoveError(ValueError):pass
class AmbiguousMoveError(ValueError):pass
Square=int
A1=0
B1=1
C1=2
D1=3
E1=4
F1=5
G1=6
H1=7
A2=8
B2=9
C2=10
D2=11
E2=12
F2=13
G2=14
H2=15
A3=16
B3=17
C3=18
D3=19
E3=20
F3=21
G3=22
H3=23
A4=24
B4=25
C4=26
D4=27
E4=28
F4=29
G4=30
H4=31
A5=32
B5=33
C5=34
D5=35
E5=36
F5=37
G5=38
H5=39
A6=40
B6=41
C6=42
D6=43
E6=44
F6=45
G6=46
H6=47
A7=48
B7=49
C7=50
D7=51
E7=52
F7=53
G7=54
H7=55
A8=56
B8=57
C8=58
D8=59
E8=60
F8=61
G8=62
H8=63
SQUARES=list(range(64))
SQUARE_NAMES=[f+r for r in RANK_NAMES for f in FILE_NAMES]
def parse_square(name):return SQUARE_NAMES.index(name)
def square_name(square):return SQUARE_NAMES[square]
def square(file_index,rank_index):return rank_index*8+file_index
def square_file(square):return square&7
def square_rank(square):return square>>3
def square_distance(a,b):return max(abs(square_file(a)-square_file(b)),abs(square_rank(a)-square_rank(b)))
def square_manhattan_distance(a,b):return abs(square_file(a)-square_file(b))+abs(square_rank(a)-square_rank(b))
def square_knight_distance(a,b):
	dx=abs(square_file(a)-square_file(b));dy=abs(square_rank(a)-square_rank(b))
	if dx+dy==1:return 3
	elif dx==dy==2:return 4
	elif dx==dy==1:
		if BB_SQUARES[a]&BB_CORNERS or BB_SQUARES[b]&BB_CORNERS:return 4
	m=math.ceil(max(dx/2,dy/2,(dx+dy)/3));return m+(m+dx+dy)%2
def square_mirror(square):return square^56
SQUARES_180=[square_mirror(sq)for sq in SQUARES]
Bitboard=int
BB_EMPTY=0
BB_ALL=0xffffffffffffffff
BB_A1=1<<A1
BB_B1=1<<B1
BB_C1=1<<C1
BB_D1=1<<D1
BB_E1=1<<E1
BB_F1=1<<F1
BB_G1=1<<G1
BB_H1=1<<H1
BB_A2=1<<A2
BB_B2=1<<B2
BB_C2=1<<C2
BB_D2=1<<D2
BB_E2=1<<E2
BB_F2=1<<F2
BB_G2=1<<G2
BB_H2=1<<H2
BB_A3=1<<A3
BB_B3=1<<B3
BB_C3=1<<C3
BB_D3=1<<D3
BB_E3=1<<E3
BB_F3=1<<F3
BB_G3=1<<G3
BB_H3=1<<H3
BB_A4=1<<A4
BB_B4=1<<B4
BB_C4=1<<C4
BB_D4=1<<D4
BB_E4=1<<E4
BB_F4=1<<F4
BB_G4=1<<G4
BB_H4=1<<H4
BB_A5=1<<A5
BB_B5=1<<B5
BB_C5=1<<C5
BB_D5=1<<D5
BB_E5=1<<E5
BB_F5=1<<F5
BB_G5=1<<G5
BB_H5=1<<H5
BB_A6=1<<A6
BB_B6=1<<B6
BB_C6=1<<C6
BB_D6=1<<D6
BB_E6=1<<E6
BB_F6=1<<F6
BB_G6=1<<G6
BB_H6=1<<H6
BB_A7=1<<A7
BB_B7=1<<B7
BB_C7=1<<C7
BB_D7=1<<D7
BB_E7=1<<E7
BB_F7=1<<F7
BB_G7=1<<G7
BB_H7=1<<H7
BB_A8=1<<A8
BB_B8=1<<B8
BB_C8=1<<C8
BB_D8=1<<D8
BB_E8=1<<E8
BB_F8=1<<F8
BB_G8=1<<G8
BB_H8=1<<H8
BB_SQUARES=[1<<sq for sq in SQUARES]
BB_CORNERS=BB_A1|BB_H1|BB_A8|BB_H8
BB_CENTER=BB_D4|BB_E4|BB_D5|BB_E5
BB_LIGHT_SQUARES=0x55aa55aa55aa55aa
BB_DARK_SQUARES=0xaa55aa55aa55aa55
BB_FILE_A=72340172838076673<<0
BB_FILE_B=72340172838076673<<1
BB_FILE_C=72340172838076673<<2
BB_FILE_D=72340172838076673<<3
BB_FILE_E=72340172838076673<<4
BB_FILE_F=72340172838076673<<5
BB_FILE_G=72340172838076673<<6
BB_FILE_H=72340172838076673<<7
BB_FILES=[BB_FILE_A,BB_FILE_B,BB_FILE_C,BB_FILE_D,BB_FILE_E,BB_FILE_F,BB_FILE_G,BB_FILE_H]
BB_RANK_1=255<<8*0
BB_RANK_2=255<<8*1
BB_RANK_3=255<<8*2
BB_RANK_4=255<<8*3
BB_RANK_5=255<<8*4
BB_RANK_6=255<<8*5
BB_RANK_7=255<<8*6
BB_RANK_8=255<<8*7
BB_RANKS=[BB_RANK_1,BB_RANK_2,BB_RANK_3,BB_RANK_4,BB_RANK_5,BB_RANK_6,BB_RANK_7,BB_RANK_8]
BB_BACKRANKS=BB_RANK_1|BB_RANK_8
def lsb(bb):return(bb&-bb).bit_length()-1
def scan_forward(bb):
	while bb:r=bb&-bb;yield r.bit_length()-1;bb^=r
def msb(bb):return bb.bit_length()-1
def scan_reversed(bb):
	while bb:r=bb.bit_length()-1;yield r;bb^=BB_SQUARES[r]
popcount=getattr(int,'bit_count',lambda bb:bin(bb).count('1'))
def flip_vertical(bb):bb=bb>>8&0xff00ff00ff00ff|(bb&0xff00ff00ff00ff)<<8;bb=bb>>16&0xffff0000ffff|(bb&0xffff0000ffff)<<16;bb=bb>>32|(bb&4294967295)<<32;return bb
def flip_horizontal(bb):bb=bb>>1&0x5555555555555555|(bb&0x5555555555555555)<<1;bb=bb>>2&0x3333333333333333|(bb&0x3333333333333333)<<2;bb=bb>>4&0xf0f0f0f0f0f0f0f|(bb&0xf0f0f0f0f0f0f0f)<<4;return bb
def flip_diagonal(bb):t=(bb^bb<<28)&0xf0f0f0f00000000;bb=bb^t^t>>28;t=(bb^bb<<14)&0x3333000033330000;bb=bb^t^t>>14;t=(bb^bb<<7)&0x5500550055005500;bb=bb^t^t>>7;return bb
def flip_anti_diagonal(bb):t=bb^bb<<36;bb=bb^(t^bb>>36)&0xf0f0f0f00f0f0f0f;t=(bb^bb<<18)&0xcccc0000cccc0000;bb=bb^t^t>>18;t=(bb^bb<<9)&0xaa00aa00aa00aa00;bb=bb^t^t>>9;return bb
def shift_down(b):return b>>8
def shift_2_down(b):return b>>16
def shift_up(b):return b<<8&BB_ALL
def shift_2_up(b):return b<<16&BB_ALL
def shift_right(b):return b<<1&~BB_FILE_A&BB_ALL
def shift_2_right(b):return b<<2&~BB_FILE_A&~BB_FILE_B&BB_ALL
def shift_left(b):return b>>1&~BB_FILE_H
def shift_2_left(b):return b>>2&~BB_FILE_G&~BB_FILE_H
def shift_up_left(b):return b<<7&~BB_FILE_H&BB_ALL
def shift_up_right(b):return b<<9&~BB_FILE_A&BB_ALL
def shift_down_left(b):return b>>9&~BB_FILE_H
def shift_down_right(b):return b>>7&~BB_FILE_A
def _sliding_attacks(square,occupied,deltas):
	attacks=BB_EMPTY
	for delta in deltas:
		sq=square
		while True:
			sq+=delta
			if not 0<=sq<64 or square_distance(sq,sq-delta)>2:break
			attacks|=BB_SQUARES[sq]
			if occupied&BB_SQUARES[sq]:break
	return attacks
def _step_attacks(square,deltas):return _sliding_attacks(square,BB_ALL,deltas)
BB_KNIGHT_ATTACKS=[_step_attacks(sq,[17,15,10,6,-17,-15,-10,-6])for sq in SQUARES]
BB_KING_ATTACKS=[_step_attacks(sq,[9,8,7,1,-9,-8,-7,-1])for sq in SQUARES]
BB_PAWN_ATTACKS=[[_step_attacks(sq,deltas)for sq in SQUARES]for deltas in[[-7,-9],[7,9]]]
def _edges(square):return(BB_RANK_1|BB_RANK_8)&~BB_RANKS[square_rank(square)]|(BB_FILE_A|BB_FILE_H)&~BB_FILES[square_file(square)]
def _carry_rippler(mask):
	subset=BB_EMPTY
	while True:
		yield subset;subset=subset-mask&mask
		if not subset:break
def _attack_table(deltas):
	mask_table=[];attack_table=[]
	for square in SQUARES:
		attacks={};mask=_sliding_attacks(square,0,deltas)&~_edges(square)
		for subset in _carry_rippler(mask):attacks[subset]=_sliding_attacks(square,subset,deltas)
		attack_table.append(attacks);mask_table.append(mask)
	return mask_table,attack_table
BB_DIAG_MASKS,BB_DIAG_ATTACKS=_attack_table([-9,-7,7,9])
BB_FILE_MASKS,BB_FILE_ATTACKS=_attack_table([-8,8])
BB_RANK_MASKS,BB_RANK_ATTACKS=_attack_table([-1,1])
def _rays():
	rays=[]
	for(a,bb_a)in enumerate(BB_SQUARES):
		rays_row=[]
		for(b,bb_b)in enumerate(BB_SQUARES):
			if BB_DIAG_ATTACKS[a][0]&bb_b:rays_row.append(BB_DIAG_ATTACKS[a][0]&BB_DIAG_ATTACKS[b][0]|bb_a|bb_b)
			elif BB_RANK_ATTACKS[a][0]&bb_b:rays_row.append(BB_RANK_ATTACKS[a][0]|bb_a)
			elif BB_FILE_ATTACKS[a][0]&bb_b:rays_row.append(BB_FILE_ATTACKS[a][0]|bb_a)
			else:rays_row.append(BB_EMPTY)
		rays.append(rays_row)
	return rays
BB_RAYS=_rays()
def ray(a,b):return BB_RAYS[a][b]
def between(a,b):bb=BB_RAYS[a][b]&(BB_ALL<<a^BB_ALL<<b);return bb&bb-1
SAN_REGEX=re.compile('^([NBKRQ])?([a-h])?([1-8])?[\\-x]?([a-h][1-8])(=?[nbrqkNBRQK])?[\\+#]?\\Z')
FEN_CASTLING_REGEX=re.compile('^(?:-|[KQABCDEFGH]{0,2}[kqabcdefgh]{0,2})\\Z')
@dataclasses.dataclass
class Piece:
	piece_type:PieceType;color:Color
	def symbol(self):symbol=piece_symbol(self.piece_type);return symbol.upper()if self.color else symbol
	def __hash__(self):return self.piece_type+(-1 if self.color else 5)
	def __repr__(self):return f"Piece.from_symbol({self.symbol()!r})"
	def __str__(self):return self.symbol()
	@classmethod
	def from_symbol(cls,symbol):return cls(PIECE_SYMBOLS.index(symbol.lower()),symbol.isupper())
@dataclasses.dataclass(unsafe_hash=True)
class Move:
	from_square:Square;to_square:Square;promotion:Optional[PieceType]=None;drop:Optional[PieceType]=None
	def uci(self):
		if self.drop:return piece_symbol(self.drop).upper()+'@'+SQUARE_NAMES[self.to_square]
		elif self.promotion:return SQUARE_NAMES[self.from_square]+SQUARE_NAMES[self.to_square]+piece_symbol(self.promotion)
		elif self:return SQUARE_NAMES[self.from_square]+SQUARE_NAMES[self.to_square]
		else:return'0000'
	def xboard(self):return self.uci()if self else'@@@@'
	def __bool__(self):return bool(self.from_square or self.to_square or self.promotion or self.drop)
	def __repr__(self):return f"Move.from_uci({self.uci()!r})"
	def __str__(self):return self.uci()
	@classmethod
	def from_uci(cls,uci):
		if uci=='0000':return cls.null()
		elif len(uci)==4 and'@'==uci[1]:
			try:drop=PIECE_SYMBOLS.index(uci[0].lower());square=SQUARE_NAMES.index(uci[2:])
			except ValueError:raise InvalidMoveError(f"invalid uci: {uci!r}")
			return cls(square,square,drop=drop)
		elif 4<=len(uci)<=5:
			try:from_square=SQUARE_NAMES.index(uci[0:2]);to_square=SQUARE_NAMES.index(uci[2:4]);promotion=PIECE_SYMBOLS.index(uci[4])if len(uci)==5 else None
			except ValueError:raise InvalidMoveError(f"invalid uci: {uci!r}")
			if from_square==to_square and from_square!=A1:raise InvalidMoveError(f"invalid uci (use 0000 for null moves): {uci!r}")
			return cls(from_square,to_square,promotion=promotion)
		else:raise InvalidMoveError(f"expected uci string to be of length 4 or 5: {uci!r}")
	@classmethod
	def null(cls):return cls(0,0)
BaseBoardT=TypeVar('BaseBoardT',bound='BaseBoard')
class BaseBoard:
	def __init__(self,board_fen=STARTING_BOARD_FEN):
		self.occupied_co=[BB_EMPTY,BB_EMPTY]
		if board_fen is None:self._clear_board()
		elif board_fen==STARTING_BOARD_FEN:self._reset_board()
		else:self._set_board_fen(board_fen)
	def _reset_board(self):self.pawns=BB_RANK_2|BB_RANK_7;self.knights=BB_B1|BB_G1|BB_B8|BB_G8;self.bishops=BB_C1|BB_F1|BB_C8|BB_F8;self.rooks=BB_CORNERS;self.queens=BB_D1|BB_D8;self.kings=BB_E1|BB_E8;self.promoted=BB_EMPTY;self.occupied_co[WHITE]=BB_RANK_1|BB_RANK_2;self.occupied_co[BLACK]=BB_RANK_7|BB_RANK_8;self.occupied=BB_RANK_1|BB_RANK_2|BB_RANK_7|BB_RANK_8
	def reset_board(self):self._reset_board()
	def _clear_board(self):self.pawns=BB_EMPTY;self.knights=BB_EMPTY;self.bishops=BB_EMPTY;self.rooks=BB_EMPTY;self.queens=BB_EMPTY;self.kings=BB_EMPTY;self.promoted=BB_EMPTY;self.occupied_co[WHITE]=BB_EMPTY;self.occupied_co[BLACK]=BB_EMPTY;self.occupied=BB_EMPTY
	def clear_board(self):self._clear_board()
	def pieces_mask(self,piece_type,color):
		if piece_type==PAWN:bb=self.pawns
		elif piece_type==KNIGHT:bb=self.knights
		elif piece_type==BISHOP:bb=self.bishops
		elif piece_type==ROOK:bb=self.rooks
		elif piece_type==QUEEN:bb=self.queens
		elif piece_type==KING:bb=self.kings
		else:assert False,f"expected PieceType, got {piece_type!r}"
		return bb&self.occupied_co[color]
	def pieces(self,piece_type,color):return SquareSet(self.pieces_mask(piece_type,color))
	def piece_at(self,square):
		piece_type=self.piece_type_at(square)
		if piece_type:mask=BB_SQUARES[square];color=bool(self.occupied_co[WHITE]&mask);return Piece(piece_type,color)
		else:return None
	def piece_type_at(self,square):
		mask=BB_SQUARES[square]
		if not self.occupied&mask:return None
		elif self.pawns&mask:return PAWN
		elif self.knights&mask:return KNIGHT
		elif self.bishops&mask:return BISHOP
		elif self.rooks&mask:return ROOK
		elif self.queens&mask:return QUEEN
		else:return KING
	def color_at(self,square):
		mask=BB_SQUARES[square]
		if self.occupied_co[WHITE]&mask:return WHITE
		elif self.occupied_co[BLACK]&mask:return BLACK
		else:return None
	def king(self,color):king_mask=self.occupied_co[color]&self.kings&~self.promoted;return msb(king_mask)if king_mask else None
	def attacks_mask(self,square):
		bb_square=BB_SQUARES[square]
		if bb_square&self.pawns:color=bool(bb_square&self.occupied_co[WHITE]);return BB_PAWN_ATTACKS[color][square]
		elif bb_square&self.knights:return BB_KNIGHT_ATTACKS[square]
		elif bb_square&self.kings:return BB_KING_ATTACKS[square]
		else:
			attacks=0
			if bb_square&self.bishops or bb_square&self.queens:attacks=BB_DIAG_ATTACKS[square][BB_DIAG_MASKS[square]&self.occupied]
			if bb_square&self.rooks or bb_square&self.queens:attacks|=BB_RANK_ATTACKS[square][BB_RANK_MASKS[square]&self.occupied]|BB_FILE_ATTACKS[square][BB_FILE_MASKS[square]&self.occupied]
			return attacks
	def attacks(self,square):return SquareSet(self.attacks_mask(square))
	def attackers_mask(self,color,square,occupied=None):occupied=self.occupied if occupied is None else occupied;rank_pieces=BB_RANK_MASKS[square]&occupied;file_pieces=BB_FILE_MASKS[square]&occupied;diag_pieces=BB_DIAG_MASKS[square]&occupied;queens_and_rooks=self.queens|self.rooks;queens_and_bishops=self.queens|self.bishops;attackers=BB_KING_ATTACKS[square]&self.kings|BB_KNIGHT_ATTACKS[square]&self.knights|BB_RANK_ATTACKS[square][rank_pieces]&queens_and_rooks|BB_FILE_ATTACKS[square][file_pieces]&queens_and_rooks|BB_DIAG_ATTACKS[square][diag_pieces]&queens_and_bishops|BB_PAWN_ATTACKS[not color][square]&self.pawns;return attackers&self.occupied_co[color]
	def is_attacked_by(self,color,square,occupied=None):return bool(self.attackers_mask(color,square,None if occupied is None else SquareSet(occupied).mask))
	def attackers(self,color,square,occupied=None):return SquareSet(self.attackers_mask(color,square,None if occupied is None else SquareSet(occupied).mask))
	def pin_mask(self,color,square):
		king=self.king(color)
		if king is None:return BB_ALL
		square_mask=BB_SQUARES[square]
		for(attacks,sliders)in[(BB_FILE_ATTACKS,self.rooks|self.queens),(BB_RANK_ATTACKS,self.rooks|self.queens),(BB_DIAG_ATTACKS,self.bishops|self.queens)]:
			rays=attacks[king][0]
			if rays&square_mask:
				snipers=rays&sliders&self.occupied_co[not color]
				for sniper in scan_reversed(snipers):
					if between(sniper,king)&(self.occupied|square_mask)==square_mask:return ray(king,sniper)
				break
		return BB_ALL
	def pin(self,color,square):return SquareSet(self.pin_mask(color,square))
	def is_pinned(self,color,square):return self.pin_mask(color,square)!=BB_ALL
	def _remove_piece_at(self,square):
		piece_type=self.piece_type_at(square);mask=BB_SQUARES[square]
		if piece_type==PAWN:self.pawns^=mask
		elif piece_type==KNIGHT:self.knights^=mask
		elif piece_type==BISHOP:self.bishops^=mask
		elif piece_type==ROOK:self.rooks^=mask
		elif piece_type==QUEEN:self.queens^=mask
		elif piece_type==KING:self.kings^=mask
		else:return None
		self.occupied^=mask;self.occupied_co[WHITE]&=~mask;self.occupied_co[BLACK]&=~mask;self.promoted&=~mask;return piece_type
	def remove_piece_at(self,square):color=bool(self.occupied_co[WHITE]&BB_SQUARES[square]);piece_type=self._remove_piece_at(square);return Piece(piece_type,color)if piece_type else None
	def _set_piece_at(self,square,piece_type,color,promoted=False):
		self._remove_piece_at(square);mask=BB_SQUARES[square]
		if piece_type==PAWN:self.pawns|=mask
		elif piece_type==KNIGHT:self.knights|=mask
		elif piece_type==BISHOP:self.bishops|=mask
		elif piece_type==ROOK:self.rooks|=mask
		elif piece_type==QUEEN:self.queens|=mask
		elif piece_type==KING:self.kings|=mask
		else:return
		self.occupied^=mask;self.occupied_co[color]^=mask
		if promoted:self.promoted^=mask
	def set_piece_at(self,square,piece,promoted=False):
		if piece is None:self._remove_piece_at(square)
		else:self._set_piece_at(square,piece.piece_type,piece.color,promoted)
	def board_fen(self,*,promoted=False):
		builder=[];empty=0
		for square in SQUARES_180:
			piece=self.piece_at(square)
			if not piece:empty+=1
			else:
				if empty:builder.append(str(empty));empty=0
				builder.append(piece.symbol())
				if promoted and BB_SQUARES[square]&self.promoted:builder.append('~')
			if BB_SQUARES[square]&BB_FILE_H:
				if empty:builder.append(str(empty));empty=0
				if square!=H1:builder.append('/')
		return''.join(builder)
	def _set_board_fen(self,fen):
		fen=fen.strip()
		if' 'in fen:raise ValueError(f"expected position part of fen, got multiple parts: {fen!r}")
		rows=fen.split('/')
		if len(rows)!=8:raise ValueError(f"expected 8 rows in position part of fen: {fen!r}")
		for row in rows:
			field_sum=0;previous_was_digit=False;previous_was_piece=False
			for c in row:
				if c in['1','2','3','4','5','6','7','8']:
					if previous_was_digit:raise ValueError(f"two subsequent digits in position part of fen: {fen!r}")
					field_sum+=int(c);previous_was_digit=True;previous_was_piece=False
				elif c=='~':
					if not previous_was_piece:raise ValueError(f"'~' not after piece in position part of fen: {fen!r}")
					previous_was_digit=False;previous_was_piece=False
				elif c.lower()in PIECE_SYMBOLS:field_sum+=1;previous_was_digit=False;previous_was_piece=True
				else:raise ValueError(f"invalid character in position part of fen: {fen!r}")
			if field_sum!=8:raise ValueError(f"expected 8 columns per row in position part of fen: {fen!r}")
		self._clear_board();square_index=0
		for c in fen:
			if c in['1','2','3','4','5','6','7','8']:square_index+=int(c)
			elif c.lower()in PIECE_SYMBOLS:piece=Piece.from_symbol(c);self._set_piece_at(SQUARES_180[square_index],piece.piece_type,piece.color);square_index+=1
			elif c=='~':self.promoted|=BB_SQUARES[SQUARES_180[square_index-1]]
	def set_board_fen(self,fen):self._set_board_fen(fen)
	def piece_map(self,*,mask=BB_ALL):
		result={}
		for square in scan_reversed(self.occupied&mask):result[square]=typing.cast(Piece,self.piece_at(square))
		return result
	def _set_piece_map(self,pieces):
		self._clear_board()
		for(square,piece)in pieces.items():self._set_piece_at(square,piece.piece_type,piece.color)
	def set_piece_map(self,pieces):self._set_piece_map(pieces)
	def _set_chess960_pos(self,scharnagl):
		if not 0<=scharnagl<=959:raise ValueError(f"chess960 position index not 0 <= {scharnagl!r} <= 959")
		n,bw=divmod(scharnagl,4);n,bb=divmod(n,4);n,q=divmod(n,6);n1=0;n2=0
		for n1 in range(0,4):
			n2=n+(3-n1)*(4-n1)//2-5
			if n1<n2 and 1<=n2<=4:break
		bw_file=bw*2+1;bb_file=bb*2;self.bishops=(BB_FILES[bw_file]|BB_FILES[bb_file])&BB_BACKRANKS;q_file=q;q_file+=int(min(bw_file,bb_file)<=q_file);q_file+=int(max(bw_file,bb_file)<=q_file);self.queens=BB_FILES[q_file]&BB_BACKRANKS;used=[bw_file,bb_file,q_file];self.knights=BB_EMPTY
		for i in range(0,8):
			if i not in used:
				if n1==0 or n2==0:self.knights|=BB_FILES[i]&BB_BACKRANKS;used.append(i)
				n1-=1;n2-=1
		for i in range(0,8):
			if i not in used:self.rooks=BB_FILES[i]&BB_BACKRANKS;used.append(i);break
		for i in range(1,8):
			if i not in used:self.kings=BB_FILES[i]&BB_BACKRANKS;used.append(i);break
		for i in range(2,8):
			if i not in used:self.rooks|=BB_FILES[i]&BB_BACKRANKS;break
		self.pawns=BB_RANK_2|BB_RANK_7;self.occupied_co[WHITE]=BB_RANK_1|BB_RANK_2;self.occupied_co[BLACK]=BB_RANK_7|BB_RANK_8;self.occupied=BB_RANK_1|BB_RANK_2|BB_RANK_7|BB_RANK_8;self.promoted=BB_EMPTY
	def set_chess960_pos(self,scharnagl):self._set_chess960_pos(scharnagl)
	def chess960_pos(self):
		if self.occupied_co[WHITE]!=BB_RANK_1|BB_RANK_2:return None
		if self.occupied_co[BLACK]!=BB_RANK_7|BB_RANK_8:return None
		if self.pawns!=BB_RANK_2|BB_RANK_7:return None
		if self.promoted:return None
		brnqk=[self.bishops,self.rooks,self.knights,self.queens,self.kings]
		if[popcount(pieces)for pieces in brnqk]!=[4,4,4,2,2]:return None
		if any((BB_RANK_1&pieces)<<56!=BB_RANK_8&pieces for pieces in brnqk):return None
		x=self.bishops&2+8+32+128
		if not x:return None
		bs1=(lsb(x)-1)//2;cc_pos=bs1;x=self.bishops&1+4+16+64
		if not x:return None
		bs2=lsb(x)*2;cc_pos+=bs2;q=0;qf=False;n0=0;n1=0;n0f=False;n1f=False;rf=0;n0s=[0,4,7,9]
		for square in range(A1,H1+1):
			bb=BB_SQUARES[square]
			if bb&self.queens:qf=True
			elif bb&self.rooks or bb&self.kings:
				if bb&self.kings:
					if rf!=1:return None
				else:rf+=1
				if not qf:q+=1
				if not n0f:n0+=1
				elif not n1f:n1+=1
			elif bb&self.knights:
				if not qf:q+=1
				if not n0f:n0f=True
				elif not n1f:n1f=True
		if n0<4 and n1f and qf:cc_pos+=q*16;krn=n0s[n0]+n1;cc_pos+=krn*96;return cc_pos
		else:return None
	def __repr__(self):return f"{type(self).__name__}({self.board_fen()!r})"
	def __str__(self):
		builder=[]
		for square in SQUARES_180:
			piece=self.piece_at(square)
			if piece:builder.append(piece.symbol())
			else:builder.append('.')
			if BB_SQUARES[square]&BB_FILE_H:
				if square!=H1:builder.append('\n')
			else:builder.append(' ')
		return''.join(builder)
	def __eq__(self,board):
		if isinstance(board,BaseBoard):return self.occupied==board.occupied and self.occupied_co[WHITE]==board.occupied_co[WHITE]and self.pawns==board.pawns and self.knights==board.knights and self.bishops==board.bishops and self.rooks==board.rooks and self.queens==board.queens and self.kings==board.kings
		else:return NotImplemented
	def apply_transform(self,f):self.pawns=f(self.pawns);self.knights=f(self.knights);self.bishops=f(self.bishops);self.rooks=f(self.rooks);self.queens=f(self.queens);self.kings=f(self.kings);self.occupied_co[WHITE]=f(self.occupied_co[WHITE]);self.occupied_co[BLACK]=f(self.occupied_co[BLACK]);self.occupied=f(self.occupied);self.promoted=f(self.promoted)
	def transform(self,f):board=self.copy();board.apply_transform(f);return board
	def apply_mirror(self):self.apply_transform(flip_vertical);self.occupied_co[WHITE],self.occupied_co[BLACK]=self.occupied_co[BLACK],self.occupied_co[WHITE]
	def mirror(self):board=self.copy();board.apply_mirror();return board
	def copy(self):board=type(self)(None);board.pawns=self.pawns;board.knights=self.knights;board.bishops=self.bishops;board.rooks=self.rooks;board.queens=self.queens;board.kings=self.kings;board.occupied_co[WHITE]=self.occupied_co[WHITE];board.occupied_co[BLACK]=self.occupied_co[BLACK];board.occupied=self.occupied;board.promoted=self.promoted;return board
	def __copy__(self):return self.copy()
	def __deepcopy__(self,memo):board=self.copy();memo[id(self)]=board;return board
	@classmethod
	def empty(cls):return cls(None)
	@classmethod
	def from_chess960_pos(cls,scharnagl):board=cls.empty();board.set_chess960_pos(scharnagl);return board
BoardT=TypeVar('BoardT',bound='Board')
class _BoardState:
	def __init__(self,board):self.pawns=board.pawns;self.knights=board.knights;self.bishops=board.bishops;self.rooks=board.rooks;self.queens=board.queens;self.kings=board.kings;self.occupied_w=board.occupied_co[WHITE];self.occupied_b=board.occupied_co[BLACK];self.occupied=board.occupied;self.promoted=board.promoted;self.turn=board.turn;self.castling_rights=board.castling_rights;self.ep_square=board.ep_square;self.halfmove_clock=board.halfmove_clock;self.fullmove_number=board.fullmove_number
	def restore(self,board):board.pawns=self.pawns;board.knights=self.knights;board.bishops=self.bishops;board.rooks=self.rooks;board.queens=self.queens;board.kings=self.kings;board.occupied_co[WHITE]=self.occupied_w;board.occupied_co[BLACK]=self.occupied_b;board.occupied=self.occupied;board.promoted=self.promoted;board.turn=self.turn;board.castling_rights=self.castling_rights;board.ep_square=self.ep_square;board.halfmove_clock=self.halfmove_clock;board.fullmove_number=self.fullmove_number
class Board(BaseBoard):
	aliases:ClassVar[List[str]]=['Standard','Chess','Classical','Normal','Illegal','From Position'];uci_variant:ClassVar[Optional[str]]='chess';xboard_variant:ClassVar[Optional[str]]='normal';starting_fen:ClassVar[str]=STARTING_FEN;tbw_suffix:ClassVar[Optional[str]]='.rtbw';tbz_suffix:ClassVar[Optional[str]]='.rtbz';tbw_magic:ClassVar[Optional[bytes]]=b'q\xe8#]';tbz_magic:ClassVar[Optional[bytes]]=b'\xd7f\x0c\xa5';pawnless_tbw_suffix:ClassVar[Optional[str]]=None;pawnless_tbz_suffix:ClassVar[Optional[str]]=None;pawnless_tbw_magic:ClassVar[Optional[bytes]]=None;pawnless_tbz_magic:ClassVar[Optional[bytes]]=None;connected_kings:ClassVar[bool]=False;one_king:ClassVar[bool]=True;captures_compulsory:ClassVar[bool]=False;turn:Color;castling_rights:Bitboard;ep_square:Optional[Square];fullmove_number:int;halfmove_clock:int;promoted:Bitboard;chess960:bool;move_stack:List[Move]
	def __init__(self,fen=STARTING_FEN,*,chess960=False):
		BaseBoard.__init__(self,None);self.chess960=chess960;self.ep_square=None;self.move_stack=[];self._stack=[]
		if fen is None:self.clear()
		elif fen==type(self).starting_fen:self.reset()
		else:self.set_fen(fen)
	@property
	def legal_moves(self):return LegalMoveGenerator(self)
	@property
	def pseudo_legal_moves(self):return PseudoLegalMoveGenerator(self)
	def reset(self):self.turn=WHITE;self.castling_rights=BB_CORNERS;self.ep_square=None;self.halfmove_clock=0;self.fullmove_number=1;self.reset_board()
	def reset_board(self):super().reset_board();self.clear_stack()
	def clear(self):self.turn=WHITE;self.castling_rights=BB_EMPTY;self.ep_square=None;self.halfmove_clock=0;self.fullmove_number=1;self.clear_board()
	def clear_board(self):super().clear_board();self.clear_stack()
	def clear_stack(self):self.move_stack.clear();self._stack.clear()
	def root(self):
		if self._stack:board=type(self)(None,chess960=self.chess960);self._stack[0].restore(board);return board
		else:return self.copy(stack=False)
	def ply(self):return 2*(self.fullmove_number-1)+(self.turn==BLACK)
	def remove_piece_at(self,square):piece=super().remove_piece_at(square);self.clear_stack();return piece
	def set_piece_at(self,square,piece,promoted=False):super().set_piece_at(square,piece,promoted=promoted);self.clear_stack()
	def generate_pseudo_legal_moves(self,from_mask=BB_ALL,to_mask=BB_ALL):
		our_pieces=self.occupied_co[self.turn];non_pawns=our_pieces&~self.pawns&from_mask
		for from_square in scan_reversed(non_pawns):
			moves=self.attacks_mask(from_square)&~our_pieces&to_mask
			for to_square in scan_reversed(moves):yield Move(from_square,to_square)
		if from_mask&self.kings:yield from self.generate_castling_moves(from_mask,to_mask)
		pawns=self.pawns&self.occupied_co[self.turn]&from_mask
		if not pawns:return
		capturers=pawns
		for from_square in scan_reversed(capturers):
			targets=BB_PAWN_ATTACKS[self.turn][from_square]&self.occupied_co[not self.turn]&to_mask
			for to_square in scan_reversed(targets):
				if square_rank(to_square)in[0,7]:yield Move(from_square,to_square,QUEEN);yield Move(from_square,to_square,ROOK);yield Move(from_square,to_square,BISHOP);yield Move(from_square,to_square,KNIGHT)
				else:yield Move(from_square,to_square)
		if self.turn==WHITE:single_moves=pawns<<8&~self.occupied;double_moves=single_moves<<8&~self.occupied&(BB_RANK_3|BB_RANK_4)
		else:single_moves=pawns>>8&~self.occupied;double_moves=single_moves>>8&~self.occupied&(BB_RANK_6|BB_RANK_5)
		single_moves&=to_mask;double_moves&=to_mask
		for to_square in scan_reversed(single_moves):
			from_square=to_square+(8 if self.turn==BLACK else-8)
			if square_rank(to_square)in[0,7]:yield Move(from_square,to_square,QUEEN);yield Move(from_square,to_square,ROOK);yield Move(from_square,to_square,BISHOP);yield Move(from_square,to_square,KNIGHT)
			else:yield Move(from_square,to_square)
		for to_square in scan_reversed(double_moves):from_square=to_square+(16 if self.turn==BLACK else-16);yield Move(from_square,to_square)
		if self.ep_square:yield from self.generate_pseudo_legal_ep(from_mask,to_mask)
	def generate_pseudo_legal_ep(self,from_mask=BB_ALL,to_mask=BB_ALL):
		if not self.ep_square or not BB_SQUARES[self.ep_square]&to_mask:return
		if BB_SQUARES[self.ep_square]&self.occupied:return
		capturers=self.pawns&self.occupied_co[self.turn]&from_mask&BB_PAWN_ATTACKS[not self.turn][self.ep_square]&BB_RANKS[4 if self.turn else 3]
		for capturer in scan_reversed(capturers):yield Move(capturer,self.ep_square)
	def generate_pseudo_legal_captures(self,from_mask=BB_ALL,to_mask=BB_ALL):return itertools.chain(self.generate_pseudo_legal_moves(from_mask,to_mask&self.occupied_co[not self.turn]),self.generate_pseudo_legal_ep(from_mask,to_mask))
	def checkers_mask(self):king=self.king(self.turn);return BB_EMPTY if king is None else self.attackers_mask(not self.turn,king)
	def checkers(self):return SquareSet(self.checkers_mask())
	def is_check(self):return bool(self.checkers_mask())
	def gives_check(self,move):
		self.push(move)
		try:return self.is_check()
		finally:self.pop()
	def is_into_check(self,move):
		king=self.king(self.turn)
		if king is None:return False
		checkers=self.attackers_mask(not self.turn,king)
		if checkers and move not in self._generate_evasions(king,checkers,BB_SQUARES[move.from_square],BB_SQUARES[move.to_square]):return True
		return not self._is_safe(king,self._slider_blockers(king),move)
	def was_into_check(self):king=self.king(not self.turn);return king is not None and self.is_attacked_by(self.turn,king)
	def is_pseudo_legal(self,move):
		if not move:return False
		if move.drop:return False
		piece=self.piece_type_at(move.from_square)
		if not piece:return False
		from_mask=BB_SQUARES[move.from_square];to_mask=BB_SQUARES[move.to_square]
		if not self.occupied_co[self.turn]&from_mask:return False
		if move.promotion:
			if piece!=PAWN:return False
			if self.turn==WHITE and square_rank(move.to_square)!=7:return False
			elif self.turn==BLACK and square_rank(move.to_square)!=0:return False
		if piece==KING:
			move=self._from_chess960(self.chess960,move.from_square,move.to_square)
			if move in self.generate_castling_moves():return True
		if self.occupied_co[self.turn]&to_mask:return False
		if piece==PAWN:return move in self.generate_pseudo_legal_moves(from_mask,to_mask)
		return bool(self.attacks_mask(move.from_square)&to_mask)
	def is_legal(self,move):return not self.is_variant_end()and self.is_pseudo_legal(move)and not self.is_into_check(move)
	def is_variant_end(self):return False
	def is_variant_loss(self):return False
	def is_variant_win(self):return False
	def is_variant_draw(self):return False
	def is_game_over(self,*,claim_draw=False):return self.outcome(claim_draw=claim_draw)is not None
	def result(self,*,claim_draw=False):outcome=self.outcome(claim_draw=claim_draw);return outcome.result()if outcome else'*'
	def outcome(self,*,claim_draw=False):
		if self.is_variant_loss():return Outcome(Termination.VARIANT_LOSS,not self.turn)
		if self.is_variant_win():return Outcome(Termination.VARIANT_WIN,self.turn)
		if self.is_variant_draw():return Outcome(Termination.VARIANT_DRAW,None)
		if self.is_checkmate():return Outcome(Termination.CHECKMATE,not self.turn)
		if self.is_insufficient_material():return Outcome(Termination.INSUFFICIENT_MATERIAL,None)
		if not any(self.generate_legal_moves()):return Outcome(Termination.STALEMATE,None)
		if self.is_seventyfive_moves():return Outcome(Termination.SEVENTYFIVE_MOVES,None)
		if self.is_fivefold_repetition():return Outcome(Termination.FIVEFOLD_REPETITION,None)
		if claim_draw:
			if self.can_claim_fifty_moves():return Outcome(Termination.FIFTY_MOVES,None)
			if self.can_claim_threefold_repetition():return Outcome(Termination.THREEFOLD_REPETITION,None)
		return None
	def is_checkmate(self):
		if not self.is_check():return False
		return not any(self.generate_legal_moves())
	def is_stalemate(self):
		if self.is_check():return False
		if self.is_variant_end():return False
		return not any(self.generate_legal_moves())
	def is_insufficient_material(self):return all(self.has_insufficient_material(color)for color in COLORS)
	def has_insufficient_material(self,color):
		if self.occupied_co[color]&(self.pawns|self.rooks|self.queens):return False
		if self.occupied_co[color]&self.knights:return popcount(self.occupied_co[color])<=2 and not self.occupied_co[not color]&~self.kings&~self.queens
		if self.occupied_co[color]&self.bishops:same_color=not self.bishops&BB_DARK_SQUARES or not self.bishops&BB_LIGHT_SQUARES;return same_color and not self.pawns and not self.knights
		return True
	def _is_halfmoves(self,n):return self.halfmove_clock>=n and any(self.generate_legal_moves())
	def is_seventyfive_moves(self):return self._is_halfmoves(150)
	def is_fivefold_repetition(self):return self.is_repetition(5)
	def can_claim_draw(self):return self.can_claim_fifty_moves()or self.can_claim_threefold_repetition()
	def is_fifty_moves(self):return self._is_halfmoves(100)
	def can_claim_fifty_moves(self):
		if self.is_fifty_moves():return True
		if self.halfmove_clock>=99:
			for move in self.generate_legal_moves():
				if not self.is_zeroing(move):
					self.push(move)
					try:
						if self.is_fifty_moves():return True
					finally:self.pop()
		return False
	def can_claim_threefold_repetition(self):
		transposition_key=self._transposition_key();transpositions=collections.Counter();transpositions.update((transposition_key,));switchyard=[]
		while self.move_stack:
			move=self.pop();switchyard.append(move)
			if self.is_irreversible(move):break
			transpositions.update((self._transposition_key(),))
		while switchyard:self.push(switchyard.pop())
		if transpositions[transposition_key]>=3:return True
		for move in self.generate_legal_moves():
			self.push(move)
			try:
				if transpositions[self._transposition_key()]>=2:return True
			finally:self.pop()
		return False
	def is_repetition(self,count=3):
		maybe_repetitions=1
		for state in reversed(self._stack):
			if state.occupied==self.occupied:
				maybe_repetitions+=1
				if maybe_repetitions>=count:break
		if maybe_repetitions<count:return False
		transposition_key=self._transposition_key();switchyard=[]
		try:
			while True:
				if count<=1:return True
				if len(self.move_stack)<count-1:break
				move=self.pop();switchyard.append(move)
				if self.is_irreversible(move):break
				if self._transposition_key()==transposition_key:count-=1
		finally:
			while switchyard:self.push(switchyard.pop())
		return False
	def _push_capture(self,move,capture_square,piece_type,was_promoted):pass
	def push(self,move):
		move=self._to_chess960(move);board_state=_BoardState(self);self.castling_rights=self.clean_castling_rights();self.move_stack.append(self._from_chess960(self.chess960,move.from_square,move.to_square,move.promotion,move.drop));self._stack.append(board_state);ep_square=self.ep_square;self.ep_square=None;self.halfmove_clock+=1
		if self.turn==BLACK:self.fullmove_number+=1
		if not move:self.turn=not self.turn;return
		if move.drop:self._set_piece_at(move.to_square,move.drop,self.turn);self.turn=not self.turn;return
		if self.is_zeroing(move):self.halfmove_clock=0
		from_bb=BB_SQUARES[move.from_square];to_bb=BB_SQUARES[move.to_square];promoted=bool(self.promoted&from_bb);piece_type=self._remove_piece_at(move.from_square);assert piece_type is not None,f"push() expects move to be pseudo-legal, but got {move} in {self.board_fen()}";capture_square=move.to_square;captured_piece_type=self.piece_type_at(capture_square);self.castling_rights&=~to_bb&~from_bb
		if piece_type==KING and not promoted:
			if self.turn==WHITE:self.castling_rights&=~BB_RANK_1
			else:self.castling_rights&=~BB_RANK_8
		elif captured_piece_type==KING and not self.promoted&to_bb:
			if self.turn==WHITE and square_rank(move.to_square)==7:self.castling_rights&=~BB_RANK_8
			elif self.turn==BLACK and square_rank(move.to_square)==0:self.castling_rights&=~BB_RANK_1
		if piece_type==PAWN:
			diff=move.to_square-move.from_square
			if diff==16 and square_rank(move.from_square)==1:self.ep_square=move.from_square+8
			elif diff==-16 and square_rank(move.from_square)==6:self.ep_square=move.from_square-8
			elif move.to_square==ep_square and abs(diff)in[7,9]and not captured_piece_type:down=-8 if self.turn==WHITE else 8;capture_square=move.to_square+down;captured_piece_type=self._remove_piece_at(capture_square)
		if move.promotion:promoted=True;piece_type=move.promotion
		castling=piece_type==KING and self.occupied_co[self.turn]&to_bb
		if castling:
			a_side=square_file(move.to_square)<square_file(move.from_square);self._remove_piece_at(move.from_square);self._remove_piece_at(move.to_square)
			if a_side:self._set_piece_at(C1 if self.turn==WHITE else C8,KING,self.turn);self._set_piece_at(D1 if self.turn==WHITE else D8,ROOK,self.turn)
			else:self._set_piece_at(G1 if self.turn==WHITE else G8,KING,self.turn);self._set_piece_at(F1 if self.turn==WHITE else F8,ROOK,self.turn)
		if not castling:
			was_promoted=bool(self.promoted&to_bb);self._set_piece_at(move.to_square,piece_type,self.turn,promoted)
			if captured_piece_type:self._push_capture(move,capture_square,captured_piece_type,was_promoted)
		self.turn=not self.turn
	def pop(self):move=self.move_stack.pop();self._stack.pop().restore(self);return move
	def peek(self):return self.move_stack[-1]
	def find_move(self,from_square,to_square,promotion=None):
		if promotion is None and self.pawns&BB_SQUARES[from_square]and BB_SQUARES[to_square]&BB_BACKRANKS:promotion=QUEEN
		move=self._from_chess960(self.chess960,from_square,to_square,promotion)
		if not self.is_legal(move):raise IllegalMoveError(f"no matching legal move for {move.uci()} ({SQUARE_NAMES[from_square]} -> {SQUARE_NAMES[to_square]}) in {self.fen()}")
		return move
	def castling_shredder_fen(self):
		castling_rights=self.clean_castling_rights()
		if not castling_rights:return'-'
		builder=[]
		for square in scan_reversed(castling_rights&BB_RANK_1):builder.append(FILE_NAMES[square_file(square)].upper())
		for square in scan_reversed(castling_rights&BB_RANK_8):builder.append(FILE_NAMES[square_file(square)])
		return''.join(builder)
	def castling_xfen(self):
		builder=[]
		for color in COLORS:
			king=self.king(color)
			if king is None:continue
			king_file=square_file(king);backrank=BB_RANK_1 if color==WHITE else BB_RANK_8
			for rook_square in scan_reversed(self.clean_castling_rights()&backrank):
				rook_file=square_file(rook_square);a_side=rook_file<king_file;other_rooks=self.occupied_co[color]&self.rooks&backrank&~BB_SQUARES[rook_square]
				if any((square_file(other)<rook_file)==a_side for other in scan_reversed(other_rooks)):ch=FILE_NAMES[rook_file]
				else:ch='q'if a_side else'k'
				builder.append(ch.upper()if color==WHITE else ch)
		if builder:return''.join(builder)
		else:return'-'
	def has_pseudo_legal_en_passant(self):return self.ep_square is not None and any(self.generate_pseudo_legal_ep())
	def has_legal_en_passant(self):return self.ep_square is not None and any(self.generate_legal_ep())
	def fen(self,*,shredder=False,en_passant='legal',promoted=None):return' '.join([self.epd(shredder=shredder,en_passant=en_passant,promoted=promoted),str(self.halfmove_clock),str(self.fullmove_number)])
	def shredder_fen(self,*,en_passant='legal',promoted=None):return' '.join([self.epd(shredder=True,en_passant=en_passant,promoted=promoted),str(self.halfmove_clock),str(self.fullmove_number)])
	def set_fen(self,fen):
		parts=fen.split()
		try:board_part=parts.pop(0)
		except IndexError:raise ValueError('empty fen')
		try:turn_part=parts.pop(0)
		except IndexError:turn=WHITE
		else:
			if turn_part=='w':turn=WHITE
			elif turn_part=='b':turn=BLACK
			else:raise ValueError(f"expected 'w' or 'b' for turn part of fen: {fen!r}")
		try:castling_part=parts.pop(0)
		except IndexError:castling_part='-'
		else:
			if not FEN_CASTLING_REGEX.match(castling_part):raise ValueError(f"invalid castling part in fen: {fen!r}")
		try:ep_part=parts.pop(0)
		except IndexError:ep_square=None
		else:
			try:ep_square=None if ep_part=='-'else SQUARE_NAMES.index(ep_part)
			except ValueError:raise ValueError(f"invalid en passant part in fen: {fen!r}")
		try:halfmove_part=parts.pop(0)
		except IndexError:halfmove_clock=0
		else:
			try:halfmove_clock=int(halfmove_part)
			except ValueError:raise ValueError(f"invalid half-move clock in fen: {fen!r}")
			if halfmove_clock<0:raise ValueError(f"half-move clock cannot be negative: {fen!r}")
		try:fullmove_part=parts.pop(0)
		except IndexError:fullmove_number=1
		else:
			try:fullmove_number=int(fullmove_part)
			except ValueError:raise ValueError(f"invalid fullmove number in fen: {fen!r}")
			if fullmove_number<0:raise ValueError(f"fullmove number cannot be negative: {fen!r}")
			fullmove_number=max(fullmove_number,1)
		if parts:raise ValueError(f"fen string has more parts than expected: {fen!r}")
		self._set_board_fen(board_part);self.turn=turn;self._set_castling_fen(castling_part);self.ep_square=ep_square;self.halfmove_clock=halfmove_clock;self.fullmove_number=fullmove_number;self.clear_stack()
	def _set_castling_fen(self,castling_fen):
		if not castling_fen or castling_fen=='-':self.castling_rights=BB_EMPTY;return
		if not FEN_CASTLING_REGEX.match(castling_fen):raise ValueError(f"invalid castling fen: {castling_fen!r}")
		self.castling_rights=BB_EMPTY
		for flag in castling_fen:
			color=WHITE if flag.isupper()else BLACK;flag=flag.lower();backrank=BB_RANK_1 if color==WHITE else BB_RANK_8;rooks=self.occupied_co[color]&self.rooks&backrank;king=self.king(color)
			if flag=='q':
				if king is not None and lsb(rooks)<king:self.castling_rights|=rooks&-rooks
				else:self.castling_rights|=BB_FILE_A&backrank
			elif flag=='k':
				rook=msb(rooks)
				if king is not None and king<rook:self.castling_rights|=BB_SQUARES[rook]
				else:self.castling_rights|=BB_FILE_H&backrank
			else:self.castling_rights|=BB_FILES[FILE_NAMES.index(flag)]&backrank
	def set_castling_fen(self,castling_fen):self._set_castling_fen(castling_fen);self.clear_stack()
	def set_board_fen(self,fen):super().set_board_fen(fen);self.clear_stack()
	def set_piece_map(self,pieces):super().set_piece_map(pieces);self.clear_stack()
	def set_chess960_pos(self,scharnagl):super().set_chess960_pos(scharnagl);self.chess960=True;self.turn=WHITE;self.castling_rights=self.rooks;self.ep_square=None;self.halfmove_clock=0;self.fullmove_number=1;self.clear_stack()
	def chess960_pos(self,*,ignore_turn=False,ignore_castling=False,ignore_counters=True):
		if self.ep_square:return None
		if not ignore_turn:
			if self.turn!=WHITE:return None
		if not ignore_castling:
			if self.clean_castling_rights()!=self.rooks:return None
		if not ignore_counters:
			if self.fullmove_number!=1 or self.halfmove_clock!=0:return None
		return super().chess960_pos()
	def _epd_operations(self,operations):
		epd=[];first_op=True
		for(opcode,operand)in operations.items():
			self._validate_epd_opcode(opcode)
			if not first_op:epd.append(' ')
			first_op=False;epd.append(opcode)
			if operand is None:epd.append(';')
			elif isinstance(operand,Move):epd.append(' ');epd.append(self.san(operand));epd.append(';')
			elif isinstance(operand,int):epd.append(f" {operand};")
			elif isinstance(operand,float):assert math.isfinite(operand),f"expected numeric epd operand to be finite, got: {operand}";epd.append(f" {operand};")
			elif opcode=='pv'and not isinstance(operand,str)and hasattr(operand,'__iter__'):
				position=self.copy(stack=False)
				for move in operand:epd.append(' ');epd.append(position.san_and_push(move))
				epd.append(';')
			elif opcode in['am','bm']and not isinstance(operand,str)and hasattr(operand,'__iter__'):
				for san in sorted(self.san(move)for move in operand):epd.append(' ');epd.append(san)
				epd.append(';')
			else:epd.append(' "');epd.append(str(operand).replace('\\','\\\\').replace('\t','\\t').replace('\r','\\r').replace('\n','\\n').replace('"','\\"'));epd.append('";')
		return''.join(epd)
	def epd(self,*,shredder=False,en_passant='legal',promoted=None,**operations):
		if en_passant=='fen':ep_square=self.ep_square
		elif en_passant=='xfen':ep_square=self.ep_square if self.has_pseudo_legal_en_passant()else None
		else:ep_square=self.ep_square if self.has_legal_en_passant()else None
		epd=[self.board_fen(promoted=promoted),'w'if self.turn==WHITE else'b',self.castling_shredder_fen()if shredder else self.castling_xfen(),SQUARE_NAMES[ep_square]if ep_square is not None else'-']
		if operations:epd.append(self._epd_operations(operations))
		return' '.join(epd)
	def _validate_epd_opcode(self,opcode):
		if not opcode:raise ValueError('empty string is not a valid epd opcode')
		if opcode=='-':raise ValueError('dash (-) is not a valid epd opcode')
		if not opcode[0].isalpha():raise ValueError(f"expected epd opcode to start with a letter, got: {opcode!r}")
		for blacklisted in[' ','\n','\t','\r']:
			if blacklisted in opcode:raise ValueError(f"invalid character {blacklisted!r} in epd opcode: {opcode!r}")
	def _parse_epd_ops(self,operation_part,make_board):
		operations={};state='opcode';opcode='';operand='';position=None
		for ch in itertools.chain(operation_part,[None]):
			if state=='opcode':
				if ch in[' ','\t','\r','\n']:
					if opcode=='-':opcode=''
					elif opcode:self._validate_epd_opcode(opcode);state='after_opcode'
				elif ch is None or ch==';':
					if opcode=='-':opcode=''
					elif opcode:operations[opcode]=[]if opcode in['pv','am','bm']else None;opcode=''
				else:opcode+=ch
			elif state=='after_opcode':
				if ch in[' ','\t','\r','\n']:pass
				elif ch=='"':state='string'
				elif ch is None or ch==';':
					if opcode:operations[opcode]=[]if opcode in['pv','am','bm']else None;opcode=''
					state='opcode'
				elif ch in'+-.0123456789':operand=ch;state='numeric'
				else:operand=ch;state='san'
			elif state=='numeric':
				if ch is None or ch==';':
					if'.'in operand or'e'in operand or'E'in operand:
						parsed=float(operand)
						if not math.isfinite(parsed):raise ValueError(f"invalid numeric operand for epd operation {opcode!r}: {operand!r}")
						operations[opcode]=parsed
					else:operations[opcode]=int(operand)
					opcode='';operand='';state='opcode'
				else:operand+=ch
			elif state=='string':
				if ch is None or ch=='"':operations[opcode]=operand;opcode='';operand='';state='opcode'
				elif ch=='\\':state='string_escape'
				else:operand+=ch
			elif state=='string_escape':
				if ch is None:operations[opcode]=operand;opcode='';operand='';state='opcode'
				elif ch=='r':operand+='\r';state='string'
				elif ch=='n':operand+='\n';state='string'
				elif ch=='t':operand+='\t';state='string'
				else:operand+=ch;state='string'
			elif state=='san':
				if ch is None or ch==';':
					if position is None:position=make_board()
					if opcode=='pv':
						variation=[]
						for token in operand.split():move=position.parse_xboard(token);variation.append(move);position.push(move)
						while position.move_stack:position.pop()
						operations[opcode]=variation
					elif opcode in['bm','am']:operations[opcode]=[position.parse_xboard(token)for token in operand.split()]
					else:operations[opcode]=position.parse_xboard(operand)
					opcode='';operand='';state='opcode'
				else:operand+=ch
		assert state=='opcode';return operations
	def set_epd(self,epd):
		parts=epd.strip().rstrip(';').split(None,4)
		if len(parts)>4:operations=self._parse_epd_ops(parts.pop(),lambda:type(self)(' '.join(parts)+' 0 1'));parts.append(str(operations['hmvc'])if'hmvc'in operations else'0');parts.append(str(operations['fmvn'])if'fmvn'in operations else'1');self.set_fen(' '.join(parts));return operations
		else:self.set_fen(epd);return{}
	def san(self,move):return self._algebraic(move)
	def lan(self,move):return self._algebraic(move,long=True)
	def san_and_push(self,move):return self._algebraic_and_push(move)
	def _algebraic(self,move,*,long=False):san=self._algebraic_and_push(move,long=long);self.pop();return san
	def _algebraic_and_push(self,move,*,long=False):
		san=self._algebraic_without_suffix(move,long=long);self.push(move);is_check=self.is_check();is_checkmate=is_check and self.is_checkmate()or self.is_variant_loss()or self.is_variant_win()
		if is_checkmate and move:return san+'#'
		elif is_check and move:return san+'+'
		else:return san
	def _algebraic_without_suffix(self,move,*,long=False):
		if not move:return'--'
		if move.drop:
			san=''
			if move.drop!=PAWN:san=piece_symbol(move.drop).upper()
			san+='@'+SQUARE_NAMES[move.to_square];return san
		if self.is_castling(move):
			if square_file(move.to_square)<square_file(move.from_square):return'O-O-O'
			else:return'O-O'
		piece_type=self.piece_type_at(move.from_square);assert piece_type,f"san() and lan() expect move to be legal or null, but got {move} in {self.fen()}";capture=self.is_capture(move)
		if piece_type==PAWN:san=''
		else:san=piece_symbol(piece_type).upper()
		if long:san+=SQUARE_NAMES[move.from_square]
		elif piece_type!=PAWN:
			others=0;from_mask=self.pieces_mask(piece_type,self.turn);from_mask&=~BB_SQUARES[move.from_square];to_mask=BB_SQUARES[move.to_square]
			for candidate in self.generate_legal_moves(from_mask,to_mask):others|=BB_SQUARES[candidate.from_square]
			if others:
				row,column=False,False
				if others&BB_RANKS[square_rank(move.from_square)]:column=True
				if others&BB_FILES[square_file(move.from_square)]:row=True
				else:column=True
				if column:san+=FILE_NAMES[square_file(move.from_square)]
				if row:san+=RANK_NAMES[square_rank(move.from_square)]
		elif capture:san+=FILE_NAMES[square_file(move.from_square)]
		if capture:san+='x'
		elif long:san+='-'
		san+=SQUARE_NAMES[move.to_square]
		if move.promotion:san+='='+piece_symbol(move.promotion).upper()
		return san
	def variation_san(self,variation):
		board=self.copy(stack=False);san=[]
		for move in variation:
			if not board.is_legal(move):raise IllegalMoveError(f"illegal move {move} in position {board.fen()}")
			if board.turn==WHITE:san.append(f"{board.fullmove_number}. {board.san_and_push(move)}")
			elif not san:san.append(f"{board.fullmove_number}...{board.san_and_push(move)}")
			else:san.append(board.san_and_push(move))
		return' '.join(san)
	def parse_san(self,san):
		try:
			if san in['O-O','O-O+','O-O#','0-0','0-0+','0-0#']:return next(move for move in self.generate_castling_moves()if self.is_kingside_castling(move))
			elif san in['O-O-O','O-O-O+','O-O-O#','0-0-0','0-0-0+','0-0-0#']:return next(move for move in self.generate_castling_moves()if self.is_queenside_castling(move))
		except StopIteration:raise IllegalMoveError(f"illegal san: {san!r} in {self.fen()}")
		match=SAN_REGEX.match(san)
		if not match:
			if san in['--','Z0','0000','@@@@']:return Move.null()
			elif','in san:raise InvalidMoveError(f"unsupported multi-leg move: {san!r}")
			else:raise InvalidMoveError(f"invalid san: {san!r}")
		to_square=SQUARE_NAMES.index(match.group(4));to_mask=BB_SQUARES[to_square]&~self.occupied_co[self.turn];p=match.group(5);promotion=PIECE_SYMBOLS.index(p[-1].lower())if p else None;from_mask=BB_ALL;from_file=None;from_rank=None
		if match.group(2):from_file=FILE_NAMES.index(match.group(2));from_mask&=BB_FILES[from_file]
		if match.group(3):from_rank=int(match.group(3))-1;from_mask&=BB_RANKS[from_rank]
		if match.group(1):piece_type=PIECE_SYMBOLS.index(match.group(1).lower());from_mask&=self.pieces_mask(piece_type,self.turn)
		elif from_file is not None and from_rank is not None:
			move=self.find_move(square(from_file,from_rank),to_square,promotion)
			if move.promotion==promotion:return move
			else:raise IllegalMoveError(f"missing promotion piece type: {san!r} in {self.fen()}")
		else:
			from_mask&=self.pawns
			if from_file is None:from_mask&=BB_FILES[square_file(to_square)]
		matched_move=None
		for move in self.generate_legal_moves(from_mask,to_mask):
			if move.promotion!=promotion:continue
			if matched_move:raise AmbiguousMoveError(f"ambiguous san: {san!r} in {self.fen()}")
			matched_move=move
		if not matched_move:raise IllegalMoveError(f"illegal san: {san!r} in {self.fen()}")
		return matched_move
	def push_san(self,san):move=self.parse_san(san);self.push(move);return move
	def uci(self,move,*,chess960=None):
		if chess960 is None:chess960=self.chess960
		move=self._to_chess960(move);move=self._from_chess960(chess960,move.from_square,move.to_square,move.promotion,move.drop);return move.uci()
	def parse_uci(self,uci):
		move=Move.from_uci(uci)
		if not move:return move
		move=self._to_chess960(move);move=self._from_chess960(self.chess960,move.from_square,move.to_square,move.promotion,move.drop)
		if not self.is_legal(move):raise IllegalMoveError(f"illegal uci: {uci!r} in {self.fen()}")
		return move
	def push_uci(self,uci):move=self.parse_uci(uci);self.push(move);return move
	def xboard(self,move,chess960=None):
		if chess960 is None:chess960=self.chess960
		if not chess960 or not self.is_castling(move):return move.xboard()
		elif self.is_kingside_castling(move):return'O-O'
		else:return'O-O-O'
	def parse_xboard(self,xboard):return self.parse_san(xboard)
	push_xboard=push_san
	def is_en_passant(self,move):return self.ep_square==move.to_square and bool(self.pawns&BB_SQUARES[move.from_square])and abs(move.to_square-move.from_square)in[7,9]and not self.occupied&BB_SQUARES[move.to_square]
	def is_capture(self,move):touched=BB_SQUARES[move.from_square]^BB_SQUARES[move.to_square];return bool(touched&self.occupied_co[not self.turn])or self.is_en_passant(move)
	def is_zeroing(self,move):touched=BB_SQUARES[move.from_square]^BB_SQUARES[move.to_square];return bool(touched&self.pawns or touched&self.occupied_co[not self.turn]or move.drop==PAWN)
	def _reduces_castling_rights(self,move):cr=self.clean_castling_rights();touched=BB_SQUARES[move.from_square]^BB_SQUARES[move.to_square];return bool(touched&cr or cr&BB_RANK_1 and touched&self.kings&self.occupied_co[WHITE]&~self.promoted or cr&BB_RANK_8 and touched&self.kings&self.occupied_co[BLACK]&~self.promoted)
	def is_irreversible(self,move):return self.is_zeroing(move)or self._reduces_castling_rights(move)or self.has_legal_en_passant()
	def is_castling(self,move):
		if self.kings&BB_SQUARES[move.from_square]:diff=square_file(move.from_square)-square_file(move.to_square);return abs(diff)>1 or bool(self.rooks&self.occupied_co[self.turn]&BB_SQUARES[move.to_square])
		return False
	def is_kingside_castling(self,move):return self.is_castling(move)and square_file(move.to_square)>square_file(move.from_square)
	def is_queenside_castling(self,move):return self.is_castling(move)and square_file(move.to_square)<square_file(move.from_square)
	def clean_castling_rights(self):
		if self._stack:return self.castling_rights
		castling=self.castling_rights&self.rooks;white_castling=castling&BB_RANK_1&self.occupied_co[WHITE];black_castling=castling&BB_RANK_8&self.occupied_co[BLACK]
		if not self.chess960:
			white_castling&=BB_A1|BB_H1;black_castling&=BB_A8|BB_H8
			if not self.occupied_co[WHITE]&self.kings&~self.promoted&BB_E1:white_castling=0
			if not self.occupied_co[BLACK]&self.kings&~self.promoted&BB_E8:black_castling=0
			return white_castling|black_castling
		else:
			white_king_mask=self.occupied_co[WHITE]&self.kings&BB_RANK_1&~self.promoted;black_king_mask=self.occupied_co[BLACK]&self.kings&BB_RANK_8&~self.promoted
			if not white_king_mask:white_castling=0
			if not black_king_mask:black_castling=0
			white_a_side=white_castling&-white_castling;white_h_side=BB_SQUARES[msb(white_castling)]if white_castling else 0
			if white_a_side and msb(white_a_side)>msb(white_king_mask):white_a_side=0
			if white_h_side and msb(white_h_side)<msb(white_king_mask):white_h_side=0
			black_a_side=black_castling&-black_castling;black_h_side=BB_SQUARES[msb(black_castling)]if black_castling else BB_EMPTY
			if black_a_side and msb(black_a_side)>msb(black_king_mask):black_a_side=0
			if black_h_side and msb(black_h_side)<msb(black_king_mask):black_h_side=0
			return black_a_side|black_h_side|white_a_side|white_h_side
	def has_castling_rights(self,color):backrank=BB_RANK_1 if color==WHITE else BB_RANK_8;return bool(self.clean_castling_rights()&backrank)
	def has_kingside_castling_rights(self,color):
		backrank=BB_RANK_1 if color==WHITE else BB_RANK_8;king_mask=self.kings&self.occupied_co[color]&backrank&~self.promoted
		if not king_mask:return False
		castling_rights=self.clean_castling_rights()&backrank
		while castling_rights:
			rook=castling_rights&-castling_rights
			if rook>king_mask:return True
			castling_rights&=castling_rights-1
		return False
	def has_queenside_castling_rights(self,color):
		backrank=BB_RANK_1 if color==WHITE else BB_RANK_8;king_mask=self.kings&self.occupied_co[color]&backrank&~self.promoted
		if not king_mask:return False
		castling_rights=self.clean_castling_rights()&backrank
		while castling_rights:
			rook=castling_rights&-castling_rights
			if rook<king_mask:return True
			castling_rights&=castling_rights-1
		return False
	def has_chess960_castling_rights(self):
		chess960=self.chess960;self.chess960=True;castling_rights=self.clean_castling_rights();self.chess960=chess960
		if castling_rights&~BB_CORNERS:return True
		if castling_rights&BB_RANK_1 and not self.occupied_co[WHITE]&self.kings&BB_E1:return True
		if castling_rights&BB_RANK_8 and not self.occupied_co[BLACK]&self.kings&BB_E8:return True
		return False
	def status(self):
		errors=STATUS_VALID
		if not self.occupied:errors|=STATUS_EMPTY
		if not self.occupied_co[WHITE]&self.kings:errors|=STATUS_NO_WHITE_KING
		if not self.occupied_co[BLACK]&self.kings:errors|=STATUS_NO_BLACK_KING
		if popcount(self.occupied&self.kings)>2:errors|=STATUS_TOO_MANY_KINGS
		if popcount(self.occupied_co[WHITE])>16:errors|=STATUS_TOO_MANY_WHITE_PIECES
		if popcount(self.occupied_co[BLACK])>16:errors|=STATUS_TOO_MANY_BLACK_PIECES
		if popcount(self.occupied_co[WHITE]&self.pawns)>8:errors|=STATUS_TOO_MANY_WHITE_PAWNS
		if popcount(self.occupied_co[BLACK]&self.pawns)>8:errors|=STATUS_TOO_MANY_BLACK_PAWNS
		if self.pawns&BB_BACKRANKS:errors|=STATUS_PAWNS_ON_BACKRANK
		if self.castling_rights!=self.clean_castling_rights():errors|=STATUS_BAD_CASTLING_RIGHTS
		valid_ep_square=self._valid_ep_square()
		if self.ep_square!=valid_ep_square:errors|=STATUS_INVALID_EP_SQUARE
		if self.was_into_check():errors|=STATUS_OPPOSITE_CHECK
		checkers=self.checkers_mask();our_kings=self.kings&self.occupied_co[self.turn]&~self.promoted
		if checkers:
			if popcount(checkers)>2:errors|=STATUS_TOO_MANY_CHECKERS
			if valid_ep_square is not None:
				pushed_to=valid_ep_square^A2;pushed_from=valid_ep_square^A4;occupied_before=self.occupied&~BB_SQUARES[pushed_to]|BB_SQUARES[pushed_from]
				if popcount(checkers)>1 or msb(checkers)!=pushed_to and self._attacked_for_king(our_kings,occupied_before):errors|=STATUS_IMPOSSIBLE_CHECK
			elif popcount(checkers)>2 or popcount(checkers)==2 and ray(lsb(checkers),msb(checkers))&our_kings:errors|=STATUS_IMPOSSIBLE_CHECK
		return errors
	def _valid_ep_square(self):
		if not self.ep_square:return None
		if self.turn==WHITE:ep_rank=5;pawn_mask=shift_down(BB_SQUARES[self.ep_square]);seventh_rank_mask=shift_up(BB_SQUARES[self.ep_square])
		else:ep_rank=2;pawn_mask=shift_up(BB_SQUARES[self.ep_square]);seventh_rank_mask=shift_down(BB_SQUARES[self.ep_square])
		if square_rank(self.ep_square)!=ep_rank:return None
		if not self.pawns&self.occupied_co[not self.turn]&pawn_mask:return None
		if self.occupied&BB_SQUARES[self.ep_square]:return None
		if self.occupied&seventh_rank_mask:return None
		return self.ep_square
	def is_valid(self):return self.status()==STATUS_VALID
	def _ep_skewered(self,king,capturer):
		assert self.ep_square is not None;last_double=self.ep_square+(-8 if self.turn==WHITE else 8);occupancy=self.occupied&~BB_SQUARES[last_double]&~BB_SQUARES[capturer]|BB_SQUARES[self.ep_square];horizontal_attackers=self.occupied_co[not self.turn]&(self.rooks|self.queens)
		if BB_RANK_ATTACKS[king][BB_RANK_MASKS[king]&occupancy]&horizontal_attackers:return True
		diagonal_attackers=self.occupied_co[not self.turn]&(self.bishops|self.queens)
		if BB_DIAG_ATTACKS[king][BB_DIAG_MASKS[king]&occupancy]&diagonal_attackers:return True
		return False
	def _slider_blockers(self,king):
		rooks_and_queens=self.rooks|self.queens;bishops_and_queens=self.bishops|self.queens;snipers=BB_RANK_ATTACKS[king][0]&rooks_and_queens|BB_FILE_ATTACKS[king][0]&rooks_and_queens|BB_DIAG_ATTACKS[king][0]&bishops_and_queens;blockers=0
		for sniper in scan_reversed(snipers&self.occupied_co[not self.turn]):
			b=between(king,sniper)&self.occupied
			if b and BB_SQUARES[msb(b)]==b:blockers|=b
		return blockers&self.occupied_co[self.turn]
	def _is_safe(self,king,blockers,move):
		if move.from_square==king:
			if self.is_castling(move):return True
			else:return not self.is_attacked_by(not self.turn,move.to_square)
		elif self.is_en_passant(move):return bool(self.pin_mask(self.turn,move.from_square)&BB_SQUARES[move.to_square]and not self._ep_skewered(king,move.from_square))
		else:return bool(not blockers&BB_SQUARES[move.from_square]or ray(move.from_square,move.to_square)&BB_SQUARES[king])
	def _generate_evasions(self,king,checkers,from_mask=BB_ALL,to_mask=BB_ALL):
		sliders=checkers&(self.bishops|self.rooks|self.queens);attacked=0
		for checker in scan_reversed(sliders):attacked|=ray(king,checker)&~BB_SQUARES[checker]
		if BB_SQUARES[king]&from_mask:
			for to_square in scan_reversed(BB_KING_ATTACKS[king]&~self.occupied_co[self.turn]&~attacked&to_mask):yield Move(king,to_square)
		checker=msb(checkers)
		if BB_SQUARES[checker]==checkers:
			target=between(king,checker)|checkers;yield from self.generate_pseudo_legal_moves(~self.kings&from_mask,target&to_mask)
			if self.ep_square and not BB_SQUARES[self.ep_square]&target:
				last_double=self.ep_square+(-8 if self.turn==WHITE else 8)
				if last_double==checker:yield from self.generate_pseudo_legal_ep(from_mask,to_mask)
	def generate_legal_moves(self,from_mask=BB_ALL,to_mask=BB_ALL):
		if self.is_variant_end():return
		king_mask=self.kings&self.occupied_co[self.turn]
		if king_mask:
			king=msb(king_mask);blockers=self._slider_blockers(king);checkers=self.attackers_mask(not self.turn,king)
			if checkers:
				for move in self._generate_evasions(king,checkers,from_mask,to_mask):
					if self._is_safe(king,blockers,move):yield move
			else:
				for move in self.generate_pseudo_legal_moves(from_mask,to_mask):
					if self._is_safe(king,blockers,move):yield move
		else:yield from self.generate_pseudo_legal_moves(from_mask,to_mask)
	def generate_legal_ep(self,from_mask=BB_ALL,to_mask=BB_ALL):
		if self.is_variant_end():return
		for move in self.generate_pseudo_legal_ep(from_mask,to_mask):
			if not self.is_into_check(move):yield move
	def generate_legal_captures(self,from_mask=BB_ALL,to_mask=BB_ALL):return itertools.chain(self.generate_legal_moves(from_mask,to_mask&self.occupied_co[not self.turn]),self.generate_legal_ep(from_mask,to_mask))
	def _attacked_for_king(self,path,occupied):return any(self.attackers_mask(not self.turn,sq,occupied)for sq in scan_reversed(path))
	def generate_castling_moves(self,from_mask=BB_ALL,to_mask=BB_ALL):
		if self.is_variant_end():return
		backrank=BB_RANK_1 if self.turn==WHITE else BB_RANK_8;king=self.occupied_co[self.turn]&self.kings&~self.promoted&backrank&from_mask;king&=-king
		if not king:return
		bb_c=BB_FILE_C&backrank;bb_d=BB_FILE_D&backrank;bb_f=BB_FILE_F&backrank;bb_g=BB_FILE_G&backrank
		for candidate in scan_reversed(self.clean_castling_rights()&backrank&to_mask):
			rook=BB_SQUARES[candidate];a_side=rook<king;king_to=bb_c if a_side else bb_g;rook_to=bb_d if a_side else bb_f;king_path=between(msb(king),msb(king_to));rook_path=between(candidate,msb(rook_to))
			if not((self.occupied^king^rook)&(king_path|rook_path|king_to|rook_to)or self._attacked_for_king(king_path|king,self.occupied^king)or self._attacked_for_king(king_to,self.occupied^king^rook^rook_to)):yield self._from_chess960(self.chess960,msb(king),candidate)
	def _from_chess960(self,chess960,from_square,to_square,promotion=None,drop=None):
		if not chess960 and promotion is None and drop is None:
			if from_square==E1 and self.kings&BB_E1:
				if to_square==H1:return Move(E1,G1)
				elif to_square==A1:return Move(E1,C1)
			elif from_square==E8 and self.kings&BB_E8:
				if to_square==H8:return Move(E8,G8)
				elif to_square==A8:return Move(E8,C8)
		return Move(from_square,to_square,promotion,drop)
	def _to_chess960(self,move):
		if move.from_square==E1 and self.kings&BB_E1:
			if move.to_square==G1 and not self.rooks&BB_G1:return Move(E1,H1)
			elif move.to_square==C1 and not self.rooks&BB_C1:return Move(E1,A1)
		elif move.from_square==E8 and self.kings&BB_E8:
			if move.to_square==G8 and not self.rooks&BB_G8:return Move(E8,H8)
			elif move.to_square==C8 and not self.rooks&BB_C8:return Move(E8,A8)
		return move
	def _transposition_key(self):return self.pawns,self.knights,self.bishops,self.rooks,self.queens,self.kings,self.occupied_co[WHITE],self.occupied_co[BLACK],self.turn,self.clean_castling_rights(),self.ep_square if self.has_legal_en_passant()else None
	def __repr__(self):
		if not self.chess960:return f"{type(self).__name__}({self.fen()!r})"
		else:return f"{type(self).__name__}({self.fen()!r}, chess960=True)"
	def __eq__(self,board):
		if isinstance(board,Board):return self.halfmove_clock==board.halfmove_clock and self.fullmove_number==board.fullmove_number and type(self).uci_variant==type(board).uci_variant and self._transposition_key()==board._transposition_key()
		else:return NotImplemented
	def apply_transform(self,f):super().apply_transform(f);self.clear_stack();self.ep_square=None if self.ep_square is None else msb(f(BB_SQUARES[self.ep_square]));self.castling_rights=f(self.castling_rights)
	def transform(self,f):board=self.copy(stack=False);board.apply_transform(f);return board
	def apply_mirror(self):super().apply_mirror();self.turn=not self.turn
	def mirror(self):board=self.copy();board.apply_mirror();return board
	def copy(self,*,stack=True):
		board=super().copy();board.chess960=self.chess960;board.ep_square=self.ep_square;board.castling_rights=self.castling_rights;board.turn=self.turn;board.fullmove_number=self.fullmove_number;board.halfmove_clock=self.halfmove_clock
		if stack:stack=len(self.move_stack)if stack is True else stack;board.move_stack=[copy.copy(move)for move in self.move_stack[-stack:]];board._stack=self._stack[-stack:]
		return board
	@classmethod
	def empty(cls,*,chess960=False):return cls(None,chess960=chess960)
	@classmethod
	def from_epd(cls,epd,*,chess960=False):board=cls.empty(chess960=chess960);return board,board.set_epd(epd)
	@classmethod
	def from_chess960_pos(cls,scharnagl):board=cls.empty(chess960=True);board.set_chess960_pos(scharnagl);return board
class PseudoLegalMoveGenerator:
	def __init__(self,board):self.board=board
	def __bool__(self):return any(self.board.generate_pseudo_legal_moves())
	def count(self):return len(list(self))
	def __iter__(self):return self.board.generate_pseudo_legal_moves()
	def __contains__(self,move):return self.board.is_pseudo_legal(move)
	def __repr__(self):
		builder=[]
		for move in self:
			if self.board.is_legal(move):builder.append(self.board.san(move))
			else:builder.append(self.board.uci(move))
		sans=', '.join(builder);return f"<PseudoLegalMoveGenerator at {id(self):#x} ({sans})>"
class LegalMoveGenerator:
	def __init__(self,board):self.board=board
	def __bool__(self):return any(self.board.generate_legal_moves())
	def count(self):return len(list(self))
	def __iter__(self):return self.board.generate_legal_moves()
	def __contains__(self,move):return self.board.is_legal(move)
	def __repr__(self):sans=', '.join(self.board.san(move)for move in self);return f"<LegalMoveGenerator at {id(self):#x} ({sans})>"
IntoSquareSet=Union[SupportsInt,Iterable[Square]]
class SquareSet:
	def __init__(self,squares=BB_EMPTY):
		try:self.mask=squares.__int__()&BB_ALL;return
		except AttributeError:self.mask=0
		for square in squares:self.add(square)
	def __contains__(self,square):return bool(BB_SQUARES[square]&self.mask)
	def __iter__(self):return scan_forward(self.mask)
	def __reversed__(self):return scan_reversed(self.mask)
	def __len__(self):return popcount(self.mask)
	def add(self,square):self.mask|=BB_SQUARES[square]
	def discard(self,square):self.mask&=~BB_SQUARES[square]
	def isdisjoint(self,other):return not bool(self&other)
	def issubset(self,other):return not bool(self&~SquareSet(other))
	def issuperset(self,other):return not bool(~self&other)
	def union(self,other):return self|other
	def __or__(self,other):r=SquareSet(other);r.mask|=self.mask;return r
	def intersection(self,other):return self&other
	def __and__(self,other):r=SquareSet(other);r.mask&=self.mask;return r
	def difference(self,other):return self-other
	def __sub__(self,other):r=SquareSet(other);r.mask=self.mask&~r.mask;return r
	def symmetric_difference(self,other):return self^other
	def __xor__(self,other):r=SquareSet(other);r.mask^=self.mask;return r
	def copy(self):return SquareSet(self.mask)
	def update(self,*others):
		for other in others:self|=other
	def __ior__(self,other):self.mask|=SquareSet(other).mask;return self
	def intersection_update(self,*others):
		for other in others:self&=other
	def __iand__(self,other):self.mask&=SquareSet(other).mask;return self
	def difference_update(self,other):self-=other
	def __isub__(self,other):self.mask&=~SquareSet(other).mask;return self
	def symmetric_difference_update(self,other):self^=other
	def __ixor__(self,other):self.mask^=SquareSet(other).mask;return self
	def remove(self,square):
		mask=BB_SQUARES[square]
		if self.mask&mask:self.mask^=mask
		else:raise KeyError(square)
	def pop(self):
		if not self.mask:raise KeyError('pop from empty SquareSet')
		square=lsb(self.mask);self.mask&=self.mask-1;return square
	def clear(self):self.mask=BB_EMPTY
	def carry_rippler(self):return _carry_rippler(self.mask)
	def mirror(self):return SquareSet(flip_vertical(self.mask))
	def tolist(self):
		result=[False]*64
		for square in self:result[square]=True
		return result
	def __bool__(self):return bool(self.mask)
	def __eq__(self,other):
		try:return self.mask==SquareSet(other).mask
		except(TypeError,ValueError):return NotImplemented
	def __lshift__(self,shift):return SquareSet(self.mask<<shift&BB_ALL)
	def __rshift__(self,shift):return SquareSet(self.mask>>shift)
	def __ilshift__(self,shift):self.mask=self.mask<<shift&BB_ALL;return self
	def __irshift__(self,shift):self.mask>>=shift;return self
	def __invert__(self):return SquareSet(~self.mask&BB_ALL)
	def __int__(self):return self.mask
	def __index__(self):return self.mask
	def __repr__(self):return f"SquareSet({self.mask:#021_x})"
	def __str__(self):
		builder=[]
		for square in SQUARES_180:
			mask=BB_SQUARES[square];builder.append('1'if self.mask&mask else'.')
			if not mask&BB_FILE_H:builder.append(' ')
			elif square!=H1:builder.append('\n')
		return''.join(builder)
	@classmethod
	def ray(cls,a,b):return cls(ray(a,b))
	@classmethod
	def between(cls,a,b):return cls(between(a,b))
	@classmethod
	def from_square(cls,square):return cls(BB_SQUARES[square])