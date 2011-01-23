#!/usr/bin/python
# This file is part of Altair web vulnerability scanner.
#
# Copyright(c) 2010-2011 Simone Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
# http://www.backbox.org
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
from xml.dom import minidom
import re

class Payload:
	def __init__( self, scope, data ):
		self.scope = scope
		self.data  = data;

	def copy( self ):
		return Payload( self.scope, self.data )
		
class Match:
	def __init__( self, type, data ):
		self.type = type
		self.data = data
		
	def copy( self ):
		return Match( self.type, self.data )
		
	def match( self, string ):
		if self.type == 'simple':
			return self.data in string
		elif self.type == 'regex':
			return re.match( self.data, string )
			
class KBItem:
	def __init__( self, id,name, severity, description ):
		self.id			 = id
		self.name        = name
		self.severity    = severity
		self.description = description
		self.payloads    = []
		self.matches     = []
		
	def addPayload( self, p ):
		self.payloads.append(p)
		
	def addMatch( self, m ):
		self.matches.append(m)
		
class KnowledgeBase:
	def __init__( self, filename, filter ):
		self.items  = []
		self.xmldoc = minidom.parse(filename)
		self.filter = filter
		
		items = self.xmldoc.firstChild.getElementsByTagName('item')
		for item in items:
			name  	 = item.attributes['name'].value.strip()
			id		 = item.attributes['id'].value.strip() if item.attributes.has_key('id') else '*'
			if '*' in self.filter or id in self.filter:
				severity = item.attributes['severity'].value.strip() if item.attributes.has_key('severity') else ''
				descr	 = item.getElementsByTagName('description')[0].firstChild.nodeValue if len(item.getElementsByTagName('description')) else ''
	
				kbitem = KBItem( id, name, severity, descr )
				ploads = item.getElementsByTagName('payload')
				for pload in ploads:
					scope   = pload.attributes['scope'].value.strip()
					content = pload.firstChild.nodeValue
					payload = Payload( scope, content )
					
					kbitem.addPayload(payload)
					
				matches = item.getElementsByTagName('match')
				for m in matches:
					type    = m.attributes['type'].value.strip()
					content = m.firstChild.nodeValue
					match   = Match( type, content )
					
					kbitem.addMatch(match)
			
				self.items.append(kbitem)