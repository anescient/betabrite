
import copy

class cpuStat:
	
	laststat = []

	def getStats ( self ):
		"return cpu status ( system, user + nice, total )"
		if self.laststat == []:
			self.laststat = self.getStat()
		newstat = self.getStat()
		
		delta = copy.copy( newstat )
		for i in range( len( delta ) ):
			delta[ i ] = delta[ i ] - self.laststat[ i ]
		self.laststat = newstat
		
		total = sum( delta )
		user = delta[ 0 ] + delta[ 1 ]
		system = delta[ 2 ] # + sum( delta[ 4:6 ] )
		return ( system, user, total )


	def getStat ( self ):
		statfile = file( "/proc/stat" )
		statline = statfile.readline()
		statfile.close()
		stat = statline.split()
		stat = stat[ 1:len( stat ) ] # lose the label
		for i in range( len( stat ) ):
			stat[ i ] = int( stat[ i ] )
		return stat

