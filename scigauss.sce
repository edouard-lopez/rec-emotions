// # contact: edouard.lopez+ter@gmail.com
// #########################################################
// #This program is free software; you can redistribute it and/or modify
// #it under the terms of the GNU General Public License as published by
// #the Free Software Foundation; either version 2 of the License, or
// #(at your option) any later version.
//
// #This program is distributed in the hope that it will be useful,
// #but WITHOUT ANY WARRANTY; without even the implied warranty of
// #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// #GNU General Public License for more details.
//
// #You should have received a copy of the GNU General Public License
// #along with this program; if not, write to the Free Software
// #Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
// #########################################################
clear


//les quatre prototypes:
jpt=[159 470 341 496 252 468 240 548];// prototype de la joie
spt=[215 555 322 553 270 538 271 587];//surprise
tpt=[164 418 253 406 210 403 215 430];//tritesse
dpt=[335 316 415 314 379 291 377 335];//dégout

//notre base de données: 200visages*4points
P=[83 137 123 138 104 135 102 152;
172 202 226 198 197 186 197 202;
160 161 245 168 202 153 199 189;
184 132 244 139 213 134 209 150;
170 153 207 154 186 144 186 168;
173 123 208 128 189 125 187 129;
135 246 170 246 151 238 151 262;
157 131 211 130 185 135 183 153;
179 171 235 170 206 166 206 187;
143 156 191 148 165 152 166 159;
147 101 189 103 168 97 165 118;
175 122 213 121 194 116 193 134;
184 118 215 117 201 107 200 133;
182 120 221 119 202 114 202 126;
163 173 225 177 184 179 184 201;
168 154 217 151 192 148 191 161;
169 149 230 145 196 146 199 171;
179 133 240 133 209 131 209 154;
201 132 256 132 229 133 229 151;
164 157 214 153 185 144 189 170;
165 150 211 145 184 135 185 160;
187 162 248 157 219 154 220 182;
153 113 207 114 180 115 181 131;
310 664 516 671 421 653 412 711;
177 361 230 373 191 350 193 370;
217 361 286 366 250 351 247 378;
169 368 231 373 189 362 190 375;
210 362 268 359 240 351 239 372;
243 340 388 347 322 342 316 393;
235 327 395 329 315 312 313 374;
232 305 366 307 285 296 286 341;
260 335 405 326 330 325 336 387;
252 328 402 333 323 322 322 390;
255 338 378 330 310 336 312 367;
264 314 373 311 318 309 319 368;
242 312 367 302 302 295 306 344;
267 320 378 324 321 320 318 367;
259 311 380 306 319 308 319 342;
268 337 381 339 321 330 320 380;
249 318 380 322 312 317 316 372;
263 327 387 336 328 322 321 385;
261 320 383 321 320 316 318 360;
261 346 363 346 310 340 312 384;
390 676 539 701 483 639 455 776;
353 692 501 694 421 617 422 783;
242 313 385 305 312 295 318 356;
240 360 354 368 296 351 294 392;
248 330 373 306 310 314 316 353;
244 320 377 301 309 314 310 321;
376 709 574 694 481 674 483 724;
353 633 523 654 434 630 427 678;
260 329 387 332 322 318 324 391;
255 329 381 323 316 305 318 357;
236 318 354 329 296 317 288 376;
250 334 394 322 318 318 323 375;
237 327 375 327 304 328 306 374;
243 314 386 324 313 315 310 350;
241 327 358 332 302 317 299 371;
275 291 365 301 320 302 318 322;
248 496 386 491 316 479 318 524;
406 704 535 694 467 678 470 713;
432 760 558 750 483 732 490 777;
441 755 575 741 496 733 500 767;
440 751 593 731 506 731 516 783;
407 722 565 709 481 705 485 729;
423 723 559 697 484 689 489 724;
438 681 575 660 500 652 503 688;
444 708 557 703 500 694 502 745;
446 744 554 732 502 706 503 783;
410 739 516 740 470 717 471 785;
457 742 587 738 526 725 526 784;
375 655 506 660 441 619 441 698;
556 669 710 676 638 656 638 699;
548 726 696 727 627 729 626 759;
576 683 727 675 664 664 655 730;
424 788 612 760 522 748 531 797;
520 566 676 559 586 533 590 583;
551 607 726 588 629 579 637 609;
506 597 654 586 572 573 574 603;
269 288 322 286 291 277 293 313;
197 163 213 317 225 233 165 235;
204 190 204 315 217 258 183 253;
273 155 260 278 278 223 251 218;
202 139 209 281 201 209 174 208;
205 165 212 265 234 215 186 213;
242 160 225 258 247 215 218 208;
251 179 246 267 279 230 223 220;
65 77 91 78 78 78 78 81;
296 398 439 374 355 394 365 430;
187 525 298 515 237 512 241 542;
188 348 271 349 228 365 227 381;
178 525 293 511 232 509 241 563;
197 529 316 522 244 512 245 542;
224 493 345 505 287 491 279 526;
187 548 339 552 267 533 262 577;
172 519 309 494 217 492 231 555;
191 565 319 551 241 532 249 583;
216 485 356 450 283 451 293 491;
177 466 356 493 284 495 265 561;
376 599 499 596 428 516 438 689;
361 517 484 519 435 503 435 522;
134 572 286 558 200 558 207 585;
181 553 324 529 234 518 240 546;
221 496 333 482 271 482 275 515;
187 524 312 524 246 499 245 560;
239 546 339 540 284 537 286 566;
240 565 339 559 287 556 291 588;
201 518 316 495 253 480 261 510;
219 591 336 579 273 566 277 611;
241 554 374 557 302 547 302 571;
174 489 267 484 217 462 221 510;
232 547 361 552 309 525 295 609;
270 564 384 570 346 534 335 600;
243 531 359 540 325 515 315 572;
204 620 329 614 259 594 263 651;
207 562 383 547 288 538 291 584;
234 545 402 570 328 544 312 623;
248 523 370 532 308 499 306 560;
242 512 375 506 312 490 312 546;
223 557 315 549 269 541 272 572;
245 511 374 495 311 484 314 524;
272 587 368 575 325 567 326 604;
158 591 319 630 252 575 237 634;
197 534 326 554 271 517 264 563;
189 540 367 536 282 538 282 589;
179 541 335 555 273 507 259 605;
204 480 339 478 281 484 281 520;
217 475 339 478 278 469 279 497;
223 533 349 538 288 519 289 563;
213 548 363 560 295 529 285 581;
231 516 360 524 305 494 294 562;
191 509 333 532 256 512 244 563;
160 468 346 492 250 467 246 545;
173 550 324 574 248 548 238 604;
223 493 350 514 292 484 283 521;
214 555 326 553 266 536 268 589;
246 580 348 554 285 554 293 576;
168 545 318 484 233 522 244 551;
161 555 309 523 214 534 222 563;
207 575 392 562 294 550 292 598;
193 571 338 570 261 551 261 592;
181 569 362 583 270 538 258 668;
285 486 395 484 346 467 343 506;
313 299 386 301 349 290 349 303;
216 438 309 438 256 423 256 466;
248 488 332 494 291 461 285 545;
234 501 333 507 283 489 280 527;
297 249 342 251 319 241 318 268;
261 254 310 249 280 241 281 259;
305 261 340 262 320 251 322 282;
234 556 363 558 299 532 297 593;
822 692 987 690 902 663 900 764;
378 1363 680 1391 517 1346 500 1460;
804 748 1028 740 912 686 914 822;
862 785 1039 771 951 741 959 861;
778 831 961 802 853 790 881 953;
810 741 985 762 895 695 886 814;
797 705 989 685 883 610 898 773;
741 637 972 653 846 574 841 778;
710 730 976 800 862 719 833 829;
711 743 974 704 835 680 860 885;
733 858 929 900 849 843 819 923;
792 757 972 762 876 681 873 817;
777 705 982 708 875 647 873 736;
730 806 998 804 852 755 864 844;
738 855 901 856 816 811 816 955;
475 1126 765 1128 602 1127 602 1174;
90 207 153 211 116 198 115 210;
775 718 951 721 862 673 859 736;
489 939 739 939 603 844 606 1043;
115 223 162 220 131 202 134 239;
475 1024 779 1016 635 984 633 1074;
450 1114 732 1112 582 1066 589 1175;
804 752 967 764 886 740 877 807;
776 746 945 745 858 705 852 845;
773 742 999 748 890 701 883 868;
701 824 925 806 806 774 807 836;
807 743 1006 731 903 742 904 787;
778 721 979 744 868 696 874 847;
761 765 994 764 874 739 869 812;
805 729 1036 735 913 690 905 850;
798 731 974 719 883 713 888 768;
881 763 1037 771 961 710 951 864;
756 737 963 716 843 681 852 842;
843 658 994 671 921 632 914 709;
808 828 1015 777 901 774 913 817;
805 753 1009 726 897 696 924 871;
762 749 934 755 825 739 833 784;
831 813 1009 788 921 776 929 808;
850 683 1017 677 929 622 934 713;
787 692 972 672 862 661 869 738;
852 764 1006 749 922 726 932 797;
768 748 934 744 846 700 852 811;
334 316 419 316 378 286 376 335;
294 272 354 278 324 260 324 279;
731 735 934 735 812 722 815 760;];

[n,m]=size(P); //taille de la matrice



// calcul de nos deux ratios (écartement, ouverture vers le haut ou vers le bas) à partir des coordonnées des points.
function [R]=ratio(pt)
a=pt(1)-pt(3);
b=pt(2)-pt(4);
c=pt(5)-pt(7);
d=pt(6)-pt(8);
  R(1,1)=sqrt((a)^2+(b)^2)/sqrt((c)^2+(d)^2);
  I(1,1)=pt(1)+(pt(3)-pt(1))/2
  I(1,2)=pt(2)+(pt(4)-pt(2))/2
  R(1,2)=sqrt((pt(5)-I(1,1))^2+(pt(6)-I(1,2))^2)/sqrt((pt(7)-I(1,1))^2+(pt(8)-I(1,2))^2);
endfunction


// nos quatre écart-types initiaux.
for i=1:4
  for j=1:2
	Si(i,j)=1;
	end
end

// nos quatre écart-types initiaux.
//Si(1,1)=1// ecart type sur x pour joie
//Si(1,2)=1;//ecart type sur y pour joie
//Si(2,1)=1;
//Si(2,2)=1;
//Si(3,1)=1;
//Si(3,2)=1;
//Si(4,1)=1;
//Si(4,2)=1;



// nos quatres espérance initiales = ratios prototypes
Ei(1,:)=ratio(jpt);
Ei(2,:)=ratio(spt);
Ei(3,:)=ratio(tpt);
Ei(4,:)=ratio(dpt);



// fonction de gauss3D qui calcule les degrés d'appartenance de la photo sur les quatres sous-ensembles émotionnels: joie, surprise, tristesse, dégout.
function [G]=gauss(x,y,S,E)
  for i=1:4
a=(x-E(i,1))^2
b=(y-E(i,2))^2
G(i)=exp(-(a/(2*(S(i,1)^2)))-(b/(2*(S(i,2)^2))))
end
endfunction



//transformation de la matrice P (points), en matrice R (ratios).
for i=1:n
  R(i,:)=ratio(P(i,:));
  end
R;



/////////////////////////////////////////////////////////////corrige les paramêtres de la gaussienne en fonction des nouvelles données.
function [S,E]= correction(x,y,Sv,Ev)// v pour vieux
  G=gauss(x,y,Sv,Ev)



//changement de l'espérance (ie du prototype). On le décale vers le nouveau point traité proportionnellement à son degré d'appartanance.
// équivaut à un calcul de barycentre avec pour poids le degré d'appartenance du nouveau point et celui de l'ancien prototype(=1).
 for i=1:4
  E(i,1)=(G(i)*x+Ev(i,1))/(G(i)+1)
  E(i,2)=(G(i)*y+Ev(i,2))/(G(i)+1)
 end


//changement des écart-types
for i=1:4
  S(i,1)=Sv(i,1)
  S(i,2)=Sv(i,2)
end

//des degrés d'appartenance trop faibles (max<2) indiquent que le point est laissé de côté.
//on veut éviter cette situation en aggrandissant les écart-types de nos fonctions pour qu'elles le captent mieux.
//on augmente d'autant plus les écart-types que le groupe des degrés est faible,
//mais parmi ces degrés, on augmente plus les écart-types de la fonction qui octroie au point un fort degré.
if max(G)<0.2 then
  for i=1:4
    S(i,1)=Sv(i,1)+G(i)*(1-max(G))*Sv(i,1)
    S(i,2)=Sv(i,2)+G(i)*(1-max(G))*Sv(i,2)
  end
end

// des degrés d'appartenances trop forts indiquent que les fonctions vont trop se recouper.
// on évite cette situation en baissant les écart-types.
//on diminue d'autant plus la écart-types que le groupe de degrés est fort.
//mais pour ces degrés, on diminue plus les écart-types qui correspond au plus faible.
if min(G)>0.8  then
  for i=1:4
    S(i,1)=Sv(i,1)-max(G)*(1-G(i))*Sv(i,1)
    S(i,2)=Sv(i,2)-max(G)*(1-G(i))*Sv(i,2)
 end
end
endfunction




///////////////////////////////////////////////////////////////////cacul des paramêtres finaux de la gaussienne.
function [Sf,Ef]= evolue (R,Si,Ei)// R matrice des ratios.
Sv=Si
Ev=Ei
  for i=1:n
    [S,E]=correction(R(i,1),R(i,2),Sv,Ev)
    Sv=S
    Ev=E
  end
Sf=Sv;//écart type final
Ef=Ev;//espérance finale.




x=[-1:0.1:5]';
y=[-1:0.1:5]';

for i=1:61
	for j=1:61
	G=gauss(x(i),y(j),Sf,Ef)
	Gj(i,j)=G(1);
	Gs(i,j)=G(2);
	Gt(i,j)=G(3);
	Gd(i,j)=G(4);
	end
end
//xset('colormap',graycolormap(128))
xbasc();
plot3d(x,x,Gj ,theta=-78,alpha=80, leg="x@y@degré appartenance",flag=[7 2 4]);//jaune
plot3d(x,x,Gs,theta=-78,alpha=80, leg="x@y@degré appartenance",flag=[2 2 4]);//bleu
plot3d(x,x,Gt,theta=-78,alpha=80,leg="x@y@degré appartenance",flag=[3 2 4]);//vert
plot3d(x,x,Gd,theta=-78,alpha=80,leg="x@y@degré appartenance",flag=[6 2 4]);//magenta
endfunction

[Sf,Ef]= evolue (R,Si,Ei)



//jpt=[159 470 341 496 252 468 240 548] //prototype de la joie initial
//JR(1,:)=ratio(spt);
//G=gauss(JR(1,1),JR(1,2),Sf,Ef);
//Gjjp=G(1)
//Gsjp=G(2)
//Gtjp=G(3)
//Gdjp=G(4)
//
//plot3d(JR(1,1),JR(1,2),Gjjp,-1)
//plot3d(JR(1,1),JR(1,2),Gsjp,-1)
//plot3d(JR(1,1),JR(1,2),Gtjp,-1)
//plot3d(JR(1,1),JR(1,2),Gdjp,-1)
