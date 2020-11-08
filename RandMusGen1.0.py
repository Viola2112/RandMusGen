# Random Music Generator 1.0

from random import *

def chaos(num):
    result = num
    for i in range(20):
        result = 3.9*(result)*(1-result)
    return result

def copyList(aList):
    result = []
    for element in aList:
        result.append(element)
    return result

def lastOfLast(nestedList):
    try:
        return lastOfLast(nestedList[-1])
    except:
        return nestedList

def depth(nestedList):
    try:
        return depth(nestedList[0])+1;
    except:
        return 0

class Note:

    def __init__(self,value):
        self.v = value

    def getValue(self):
        return self.v

    def repeat(self):
        return Note(self.v)

    def variation(self,seed):
        if seed < 0.5:
            return Note(self.v-1)
        return Note(self.v+1)

    def contrast(self,seed):
        if seed < 0.5:
            return Note(self.v-2)
        return Note(self.v+2)

class Measure:

    def __init__(self,noteList):
        self.nList = noteList

    def getValue(self):
        result = []
        for note in self.nList:
            result.append(note.getValue())
        return result

    def absoluteLastNote(self):
        try:
            theLast = self.nList[-1]
            return theLast.absoluteLastNote()
        except:
            return self.nList[-1]

    def depth(self):
        try:
            return 1 + self.nList[0].depth()
        except:
            return 1

    def repeat(self):
        return Measure(self.nList)

    def variation(self,seed):
        # Options:
            # Reorder notes
            # Contrast for one note
            # Same variation for all notes
        if seed < 1/3:
            # Be careful with lists here!
            newList = copyList(self.nList)
            shuffle(newList)
            return Measure(newList)
        if seed < 2/3:
            newSeed = chaos(seed)
            newList = copyList(self.nList)
            randNum = int(len(newList)*newSeed)
            newSeed = chaos(newSeed)
            newNote = newList[randNum].contrast(newSeed)
            newList[randNum] = newNote
            return Measure(newList)
        # Third Option
        newSeed = chaos(seed)
        newList = []
        for i in range(len(self.nList)):
            newList.append(self.nList[i].variation(newSeed))
        return Measure(newList)

    def contrast(self,seed):
        # Find the very last note
        # Build up measure from it until it's same depth
        theLast = self.absoluteLastNote()
        result = buildMeasure(theLast,seed)
        newSeed = chaos(seed)
        keepGoing = (result.depth() != self.depth())
        while keepGoing:
            newSeed = chaos(seed)
            result = expandMeasure(result,newSeed)
            keepGoing = (result.depth() != self.depth())
        return result
        

def buildMeasure(initNote,seed):
    noteList = []
    currNote = initNote
    newSeed = seed
    for i in range(4):
        # 1/4 chance of repeat, 1/2 chance of variation,
        # 1/4 chance of contrast
        if newSeed < 1/4:
            currNote = currNote.repeat()
        elif newSeed < 3/4:
            newSeed = chaos(newSeed)
            currNote = currNote.variation(newSeed)
        else:
            newSeed = chaos(newSeed)
            currNote = currNote.contrast(newSeed)
        noteList.append(currNote)
        newSeed = chaos(newSeed)
    return Measure(noteList)

def expandMeasure(initNote,seed):
    noteList = []
    currNote = initNote
    noteList.append(currNote)
    newSeed = seed
    for i in range(3):
        # 1/4 chance of repeat, 1/2 chance of variation,
        # 1/4 chance of contrast
        if newSeed < 1/4:
            currNote = currNote.repeat()
        elif newSeed < 3/4:
            newSeed = chaos(newSeed)
            currNote = currNote.variation(newSeed)
        else:
            newSeed = chaos(newSeed)
            currNote = currNote.contrast(newSeed)
        noteList.append(currNote)
        newSeed = chaos(newSeed)
    return Measure(noteList)
            
                
            

