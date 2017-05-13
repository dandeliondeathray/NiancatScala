package io.github.dandeliondeathray.niancat

sealed trait Response
sealed trait Reply extends Response
sealed trait Notification extends Response

case class CompositeResponse(responses: Vector[Response]) extends Response
case class NoResponse() extends Response

case class NoPuzzleSet() extends Reply
case class GetReply(puzzle: Puzzle) extends Reply {
  override def toString: String = PuzzleHelper.displayPuzzle(puzzle)
}
case class NotInTheDictionary(word: Word) extends Reply
case class CorrectSolution(word: Word) extends Reply
case class WordAndPuzzleMismatch(word: Word, puzzle: Puzzle) extends Reply
case class IncorrectLength(word: Word) extends Reply
case class InvalidPuzzle(puzzle: Puzzle) extends Reply
case class InvalidCommandReply(msg: String, invalidCommandError: InvalidCommandError) extends Reply
case class SamePuzzle(puzzle: Puzzle) extends Reply

case class NewPuzzle(puzzle: Puzzle) extends Notification {
  override def toString: String = {
    val puzzleString = PuzzleHelper.displayPuzzle(puzzle)
    s"Dagens nian är $puzzleString"
  }
}
case class YesterdaysPuzzle(result: SolutionResult) extends Notification
case class MultipleSolutions(n: Int) extends Notification

object PuzzleHelper {
  def displayPuzzle(p: Puzzle): String = {
    p.letters grouped(3) mkString(" ")
  }
}
