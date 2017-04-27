""".......This file calls the client, competitor1 and competitor2 website scraping files one by one........"""

import ellos1
import bubble1
import boozt1
import header as h

if __name__ == '__main__':

    ellos1.main()
    bubble1.main()
    boozt1.main()
    h.cur.close()
    h.conn.close()