"""

"""

import versions
from versions import argparser


__author__ = 'Grant Holmes'
__email__ = 'g.holmes429@gmail.com'
__created__ = '10/19/2021'
__modified__ = '10/21/2021'


diviner_versions = {
	'd5': versions.D5
}

def main():
	args = argparser.parse_args()
	diviner_versions[args.version](args)

if __name__ == '__main__':
	main()
