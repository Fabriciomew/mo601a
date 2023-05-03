/**
 * @file      012.const.c
 * @author    The ArchC Team
 *            http://www.archc.org/
 *
 *            Computer Systems Laboratory (LSC)
 *            IC-UNICAMP
 *            http://www.lsc.ic.unicamp.br
 *
 * @version   1.0
 * @date      Mon, 19 Jun 2006 15:33:22 -0300
 * @brief     It is a simple main function that uses unsigned char and returns 0.
 *
 * @attention Copyright (C) 2002-2006 --- The ArchC Team
 * 
 * This program is free software; you can redistribute it and/or modify 
 * it under the terms of the GNU General Public License as published by 
 * the Free Software Foundation; either version 2 of the License, or 
 * (at your option) any later version. 
 * 
 * This program is distributed in the hope that it will be useful, 
 * but WITHOUT ANY WARRANTY; without even the implied warranty of 
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 * GNU General Public License for more details. 
 * 
 * You should have received a copy of the GNU General Public License 
 * along with this program; if not, write to the Free Software 
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */

/* The file begin.h is included if compiler flag -DBEGINCODE is used */
#ifdef BEGINCODE
#include "begin.h"
#endif

int main() {
  float uc=3,ua=0;

  ua=9.0;
  /* After uc is 10.5555 */

  /* Before uc is 10.5555 */ uc/=ua; 
  /* After uc is 21.111 */

  /* Before uc is 21.111 */ uc=2.35*uc*ua + 23*uc*ua; 
  /* After uc is 10.5555 */

  /* Before uc is 10.5555 */ uc=ua/2.3467;
  /* After uc is 21.111 */

  /* Before uc is 21.111 */ uc=ua+uc+uc+ua+ua-uc-uc*ua*2; 
  /* After uc is 10.5555 */

  /* Before uc is 10.5555 */ uc=uc-uc; 
  /* After uc is 111.41858025 */

  /* Before uc is 111.41858025 */ uc=1.0;
  /* After uc is 10.5555 */

  /* Before uc is 10.5555 */ uc=uc - 1.0;
  /* After uc is 10.5555 */

  /* Before uc is 10.5555 */ return 0; 
  /* Return 0 */
}

/* The file end.h is included if compiler flag -DENDCODE is used */
#ifdef ENDCODE
#include "end.h"
#endif
