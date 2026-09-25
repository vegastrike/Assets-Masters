// ---------------------------------------------------------------------------
// Space3D
// Free POV-Ray script for space scenes rendering
// Copyright (C) 2005-2008 Pyramid
// Contact: pedrabella@sapo.pt
// Internet: http://space3d.no.sapo.pt/
//
// This script is distributed with ABSOLUTELY NO WARRANTY;
// See the GNU General Public License for more details,
// which can be found in doc/SPACE3D_LICENSE.txt
//
// Persistence of Vision Ray Tracer Scene Description File
// File       : stafield_example.pov
// Description: Development scenes for starfield.inc
// Version    : 0.16
// Date       : 2008-04-02
// Author     : Pyramid
// Internet   : http://space3d.no.sapo.pt/
// Scale      : 1 POV Unit = 1km
// ---------------------------------------------------------------------------
// There are 8 predefined skyspheres. Sample implemenmtation is scene nr. 1
// (1) USE_OBJECT_NUMBER tells the inc file to only create this object
//      1- x: star fields
//     11-16: star cluster object
//     21-24: star nebula pigment for skysphere
//     31-34: cloud nebula pigment for skysphere
//     41-42: dense cloud nebula objects
// (2) starcluster_rotation is the angular extension of the star spread
//     should have values between 0 and 180 because a random left&right
//     rotation is generated
// (3) starfield_star_intensity is the maximum intensity
// (4) starfield_distribu_angle defines the radius of a globular cluster
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Global Settings
// ---------------------------------------------------------------------------
#version 3.6;
global_settings {
   assumed_gamma 2.2
}

// ---------------------------------------------------------------------------
// User Settings
// ---------------------------------------------------------------------------

// Quality Settings for test & sample or final rendering
#declare render_quality = 1; // 0=fast/less stars; 1=full/more stars
#declare STARFIELD_SCENE_NR = 31; // range 1-31
#declare STARFIELD_NR = frame_number;
#declare CAMERA = 6; //1=normal, 2=90degree, 6=texture/unwrap

#declare show_debug = false;
#declare create_logfile = false;

// ---------------------------------------------------------------------------
// Include Files
// ---------------------------------------------------------------------------
#include "rand.inc" // random number generation macros
#include "starfield.inc"

// ---------------------------------------------------------------------------
// Macros
// ---------------------------------------------------------------------------
#macro IRand(Min,Max,Stream) (int(rand(Stream)*(Max-Min+1)) + Min) #end
#macro vRand(s) (<rand(s),rand(s),rand(s)>*2-1) #end

#macro RandomStarColor(iColor,rColor)
   #switch (iColor)
      #case (1) //redish
         color rgb <RRand(0.5,1.0,rColor), RRand(0.4,0.6,rColor), RRand(0.4,0.6,rColor)>;
      #break
      #case (2) //yellowish
         color rgb <RRand(0.5,1.0,rColor), RRand(0.5,1.0,rColor), RRand(0.4,0.6,rColor)>;
      #break
      #case (3) //blueish
         color rgb <RRand(0.4,0.6,rColor), RRand(0.4,0.6,rColor), RRand(0.5,1.0,rColor)>;
      #break
      #case (4) //random
         color rgb <RRand(0.5,1.0,rColor), RRand(0.5,1.0,rColor), RRand(0.5,1.0,rColor)>;
      #break
   #end
#end

// ---------------------------------------------------------------------------
// Lights
// ---------------------------------------------------------------------------

// general light definition
light_source {
  <1000, 1000, -100> // position of the light source
  color rgb 1.0      // color of the light
}

// ---------------------------------------------------------------------------
// Scene
// ---------------------------------------------------------------------------

//  vegastrike red_galaxy1
#if (STARFIELD_SCENE_NR = 31)
   #declare STARFIELD_NR = 13; //frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (1825 + STARFIELD_NR);
   #declare NEBULA_COLORS = array[2];
   //first test
   #declare NEBULA_COLORS[0] = color rgb <0.9235, 0.0754, 0.0375>;
   #declare NEBULA_COLORS[1] = color rgb <0.7243, 0.8491, 0.0180>;
   // other tests
   //#declare NEBULA_COLORS[0] = color rgb <RRand(0.8,1.0,rColor), RRand(0.0,0.3,rColor), RRand(0.0,0.1,rColor)>;
   //#declare NEBULA_COLORS[1] = color rgb <RRand(0.7,1.0,rColor), RRand(0.1,0.2,rColor), RRand(0.0,0.1,rColor)>;
   #if (show_debug)
     #debug concat("NEBULA_COLORS 0: ",vstr(3,NEBULA_COLORS[0],", ",0,4),"\n")
     #debug concat("NEBULA_COLORS 1: ",vstr(3,NEBULA_COLORS[1],", ",0,4),"\n")
   #end

   #declare show = 1; #if (show) 
      #declare USE_OBJECT_NUMBER = 41; #include "starfield.inc"
      #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
      object { mNebulaSelect(1,1,1,NEBULA_COLORS,0,rShape,rColor) rotate V_Rotation translate<-0.01, 0, 0> }
   
      #declare USE_OBJECT_NUMBER = 42; #include "starfield.inc"
      #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
      object { mNebulaSelect(1,2,1,NEBULA_COLORS,0,rShape,rColor) rotate V_Rotation translate<0, 0, 0> }
   #end

   #declare starfield_seed_no = 16486+STARFIELD_NR;
   #declare SeedS = seed(starfield_seed_no);

   //star streaks in the nebula - upper left
   #declare show = 1; #if (show) 
      #declare STARFIELD_NR = frame_number;
      #declare STARFIELDS_NO = 1; //IRand(4,8,SeedS);
      #declare STARFIELD=1; #while (STARFIELD<=STARFIELDS_NO)
         #declare STARFIELD_STAR_TYPE = 2; //IRand(2,4,SeedS); //1=tiny 2=small 3=medium 4=big 5=large      
         #declare starfield_star_intensity = RRand(2.0,5.0,SeedS); //maximum intensity
         #declare iColor = IRand(1,4,rColor);
         #declare starfield_star_color = RandomStarColor(iColor,rColor)
         #declare starfield_seed_no = starfield_seed_no + STARFIELD;
         #declare starcluster_excentricity = <2,0.5,1>;
         #declare starcluster_rotation = <5,5,5>;
         #declare starfield_star_amount = 1000/pow(STARFIELD_STAR_TYPE,3);
         #declare USE_OBJECT_NUMBER = 15; #include "starfield.inc"
         object { O_StarCluster05(1,rPosition) rotate <0,0,45> translate <-4e3,4e3,0>}
      #declare STARFIELD=STARFIELD+1; #end
   #end

   //star streaks in the nebula - upper right
   #declare STARFIELD_NR = frame_number;
      #declare show = 1; #if (show) 
      #declare STARFIELDS_NO = 1; //IRand(4,8,SeedS);
      #declare STARFIELD=1; #while (STARFIELD<=STARFIELDS_NO)
         #declare STARFIELD_STAR_TYPE = 2; //IRand(2,4,SeedS); //1=tiny 2=small 3=medium 4=big 5=large      
         #declare starfield_star_intensity = RRand(2.0,5.0,SeedS); //maximum intensity
         #declare iColor = IRand(1,4,rColor);
         #declare starfield_star_color = RandomStarColor(iColor,rColor)
         #declare starfield_seed_no = starfield_seed_no + STARFIELD;
         #declare starcluster_excentricity = <2,0.5,1>;
         #declare starcluster_rotation = <5,5,5>;
         #declare starfield_star_amount = 1000/pow(STARFIELD_STAR_TYPE,3);
         #declare USE_OBJECT_NUMBER = 15; #include "starfield.inc"
         object { O_StarCluster05(1,rPosition) rotate <0,0,-45> translate <4e3,4e3,0>}
      #declare STARFIELD=STARFIELD+1; #end
   #end

   //star streaks in the nebula - middle
   #declare STARFIELD_NR = frame_number;
      #declare show = 1; #if (show) 
      #declare STARFIELDS_NO = 10; //IRand(4,8,SeedS);
      #declare STARFIELD=1; #while (STARFIELD<=STARFIELDS_NO)
         #declare STARFIELD_STAR_TYPE = 2; //IRand(2,4,SeedS); //1=tiny 2=small 3=medium 4=big 5=large      
         #declare starfield_star_intensity = RRand(2.0,5.0,SeedS); //maximum intensity
         #declare iColor = IRand(1,4,rColor);
         #declare starfield_star_color = RandomStarColor(iColor,rColor)
         #declare starfield_seed_no = starfield_seed_no + STARFIELD;
         #declare starcluster_excentricity = <RRand(1.0,1.5,SeedS), RRand(1.0,1.5,SeedS), RRand(1.0,1.5,SeedS)>;
         #declare starcluster_rotation = <RRand(3,10,SeedS), RRand(3,10,SeedS), RRand(3,10,SeedS)>;
         #declare starfield_star_amount = 1000/pow(STARFIELD_STAR_TYPE,3);
         #declare USE_OBJECT_NUMBER = 15; #include "starfield.inc"
         object { O_StarCluster05(1,rPosition) rotate <0,0,0> translate <0,0,0>}
      #declare STARFIELD=STARFIELD+1; #end
   #end

   //star streaks in the nebula - middle
   #declare STARFIELD_NR = frame_number;
      #declare show = 1; #if (show) 
      #declare STARFIELDS_NO = 10; //IRand(4,8,SeedS);
      #declare STARFIELD=1; #while (STARFIELD<=STARFIELDS_NO)
         #declare STARFIELD_STAR_TYPE = 2; //IRand(2,4,SeedS); //1=tiny 2=small 3=medium 4=big 5=large      
         #declare starfield_star_intensity = RRand(2.0,5.0,SeedS); //maximum intensity
         #declare iColor = IRand(1,4,rColor);
         #declare starfield_star_color = RandomStarColor(iColor,rColor)
         #declare starfield_seed_no = starfield_seed_no + STARFIELD;
         #declare starcluster_excentricity = <RRand(1.0,1.5,SeedS), RRand(1.0,1.5,SeedS), RRand(1.0,1.5,SeedS)>;
         #declare starcluster_rotation = <RRand(3,10,SeedS), RRand(3,10,SeedS), RRand(3,10,SeedS)>;
         #declare starfield_star_amount = 1000/pow(STARFIELD_STAR_TYPE,3);
         #declare USE_OBJECT_NUMBER = 15; #include "starfield.inc"
         object { O_StarCluster05(1,rPosition) rotate <0,0,0> translate <-4e3,-4e3,0>}
      #declare STARFIELD=STARFIELD+1; #end
   #end

   //small stars
   #declare show = 1; #if (show) 
      #declare STARFIELD_NR = frame_number;
      #declare STARFIELDS_NO = 100; //IRand(4,8,SeedS);
      #declare STARFIELD=1; #while (STARFIELD<=STARFIELDS_NO)
         #declare STARFIELD_STAR_TYPE = 2; //IRand(2,4,SeedS); //1=tiny 2=small 3=medium 4=big 5=large      
         #declare starfield_star_intensity = RRand(2.0,5.0,SeedS); //maximum intensity
         #declare iColor = IRand(1,4,rColor);
         #declare starfield_star_color = RandomStarColor(iColor,rColor)
         #declare starfield_seed_no = starfield_seed_no + STARFIELD;
         #declare starcluster_excentricity = color rgb <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
         #declare starcluster_rotation = <RRand(-180,180,SeedS), RRand(-180,180,SeedS), RRand(-180,180,SeedS)>;
         #declare starfield_star_amount = 1000/pow(STARFIELD_STAR_TYPE,3);
         #declare USE_OBJECT_NUMBER = 15;
         #include "starfield.inc"
         object {O_StarCluster05(1,rPosition)}
      #declare STARFIELD=STARFIELD+1; #end
   #end

   //middle stars
   #declare show = 1; #if (show) 
      #declare STARFIELD_NR = frame_number;
      #declare STARFIELDS_NO = 10; //IRand(4,8,SeedS);
      #declare STARFIELD=1; #while (STARFIELD<=STARFIELDS_NO)
         #declare STARFIELD_STAR_TYPE = 3; //IRand(2,4,SeedS); //1=tiny 2=small 3=medium 4=big 5=large      
         #declare starfield_star_intensity = RRand(2.0,5.0,SeedS); //maximum intensity
         #declare iColor = IRand(1,4,rColor);
         #declare starfield_star_color = RandomStarColor(iColor,rColor)
         #declare starfield_seed_no = starfield_seed_no + STARFIELD;
         #declare starcluster_excentricity = color rgb <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
         #declare starcluster_rotation = <RRand(-180,180,SeedS), RRand(-180,180,SeedS), RRand(-180,180,SeedS)>;
         #declare starfield_star_amount = 1000/pow(STARFIELD_STAR_TYPE,3);
         #declare USE_OBJECT_NUMBER = 15;
         #include "starfield.inc"
         object {O_StarCluster05(1,rPosition)}
      #declare STARFIELD=STARFIELD+1; #end
   #end

   //big stars
   #declare show = 1; #if (show) 
      #declare STARFIELD_NR = frame_number;
      #declare STARFIELDS_NO = 5; //IRand(4,8,SeedS);
      #declare STARFIELD=1; #while (STARFIELD<=STARFIELDS_NO)
         #declare STARFIELD_STAR_TYPE = 4; //IRand(2,4,SeedS); //1=tiny 2=small 3=medium 4=big 5=large      
         #declare starfield_star_intensity = RRand(2.0,5.0,SeedS); //maximum intensity
         #declare iColor = IRand(1,4,rColor);
         #declare starfield_star_color = RandomStarColor(iColor,rColor)
         #declare starfield_seed_no = starfield_seed_no + STARFIELD;
         #declare starcluster_excentricity = color rgb <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
         #declare starcluster_rotation = <RRand(-180,180,SeedS), RRand(-180,180,SeedS), RRand(-180,180,SeedS)>;
         #declare starfield_star_amount = 1000/pow(STARFIELD_STAR_TYPE,3);
         #declare USE_OBJECT_NUMBER = 15;
         #include "starfield.inc"
         object {O_StarCluster05(1,rPosition)}
      #declare STARFIELD=STARFIELD+1; #end
   #end


   #declare show = 1; #if (show) 
      #declare STARFIELD_NR = frame_number;
      #declare rPosition = seed (6741 + STARFIELD_NR);
      #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
      #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
      sky_sphere { pigment { P_StarField05() } rotate V_Rotation }
   #end
#end //SCENE

//  random background scene
#if (STARFIELD_SCENE_NR = 30)
   //#declare CAMERA = 6;
   #declare STARFIELD_NR = frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (34825 + STARFIELD_NR);
   #declare rShape = seed (93265 + STARFIELD_NR);
   #declare rStarfield = seed (1000 + STARFIELD_NR);
   #declare iBackgrounds = IRand(1,2,rStarfield);
   #if (create_logfile)
      #write(LogFile,"iBackgrounds = ",iBackgrounds,"\n")
   #end
   #declare I=1; #while (I<=iBackgrounds)
      #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
      #declare iBackground = IRand(41,49,rStarfield);
      #if (iBackground=49) #local iBackground=52; #end
      #if (iBackground=45) #local iBackground=47; #end
      #if (iBackground=46) #local iBackground=47; #end
      #declare USE_OBJECT_NUMBER = iBackground;
      #if (create_logfile)
         #write(LogFile,"USE_OBJECT_NUMBER = ",USE_OBJECT_NUMBER,"\n")
      #end
      #include "starfield.inc"
      #switch (iBackground)
         #range (41,43)
            object { mCloudNebula(NEBULA_COLORS,rShape,rColor) rotate V_Rotation translate <-1*I, 0, -1*I> }
         #break
         #case (44)
            object { mCloudNebula(1,rShape,rColor) rotate V_Rotation translate <1*I, 0, 1*I> }
         #break
         #case (45)
            object { mRingNebula(1,rShape,rColor) rotate V_Rotation translate <1*I, 0, 20*I> }
         #break
         #range (46,48)
            object { mCloudNebula(1,rShape,rColor) rotate V_Rotation translate <1*I, 0, 1*I> }
         #break
         #range (51,52)
            object { mBackgroundNebula(0,rShape,rColor) rotate V_Rotation translate <1*I, 0, 0> } //0=random pattern
         #break
      #end
   #declare I=I+1; #end

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  background nebula 52
#if (STARFIELD_SCENE_NR = 29)
   //#declare CAMERA = 6;
   #declare STARFIELD_NR = frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (34825 + STARFIELD_NR);
   #declare rShape = seed (93265 + STARFIELD_NR);

   #declare USE_OBJECT_NUMBER = 52; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mBackgroundNebula(0,rShape,rColor) rotate V_Rotation translate <0, 0, 0> } //0=random pattern //1-5,(6-8),19

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  background nebula 51
#if (STARFIELD_SCENE_NR = 28)
   //#declare CAMERA = 6;
   #declare STARFIELD_NR = frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (34825 + STARFIELD_NR);
   #declare rShape = seed (93265 + STARFIELD_NR);

   #declare USE_OBJECT_NUMBER = 51; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mBackgroundNebula(1,rShape,rColor) rotate V_Rotation translate <0, 0, 0> }

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  cloud nebula 48
#if (STARFIELD_SCENE_NR = 27)
   //#declare CAMERA = 6;
   #declare STARFIELD_NR = frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (34825 + STARFIELD_NR);
   #declare rShape = seed (93265 + STARFIELD_NR);

   #declare USE_OBJECT_NUMBER = 48; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mCloudNebula(1,rShape,rColor) rotate V_Rotation translate<0, 0, 0> }

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  cloud nebula 47
#if (STARFIELD_SCENE_NR = 26)
   #declare CAMERA = 6;
   #declare STARFIELD_NR = 4; //frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (34825 + STARFIELD_NR);
   #declare rShape = seed (93265 + STARFIELD_NR);

   #declare USE_OBJECT_NUMBER = 47; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mCloudNebula(1500,rShape,rColor) rotate V_Rotation translate<0, 0, 0> }

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  cloud nebula 46
#if (STARFIELD_SCENE_NR = 25)
   #declare STARFIELD_NR = frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (34825 + STARFIELD_NR);
   #declare rShape = seed (93265 + STARFIELD_NR);

   #declare USE_OBJECT_NUMBER = 46; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mCloudNebula(1,rShape,rColor) rotate V_Rotation translate<0, 0, 0> }

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  ring nebula 45
#if (STARFIELD_SCENE_NR = 24)
   #declare STARFIELD_NR = frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (1825 + STARFIELD_NR);
   #declare rShape = seed (93265 + STARFIELD_NR);

   #declare USE_OBJECT_NUMBER = 45; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mRingNebula(1,rShape,rColor) rotate V_Rotation translate <0, 0, 20> }

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  spiral galaxy
#if (STARFIELD_SCENE_NR = 23)
   #declare rShape = seed (5619 + STARFIELD_NR);
   #declare iArms = IRand(0,5,rShape)*2;
   #declare vTurb = vRand(rShape)*100;
   #declare fSpiral = rand(rShape)*2;
   #declare fGlow = rand(rShape);
   #declare fTurb = rand(rShape)*0.7;
   #declare fColDev = rand(rShape);
   #include "spiral_galaxy.inc"
   //SpiralGalaxy(arms, Rand, spiralness, glowiness, turb, colShift)
   object { SpiralGalaxy(iArms, vTurb, fSpiral, fGlow, fTurb, fColDev) rotate <40,-30,0> translate <0,0,2> }
   
   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  dense cloud nebula 44
#if (STARFIELD_SCENE_NR = 22)
   #declare STARFIELD_NR = frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (1825 + STARFIELD_NR);
   #declare rShape = seed (5619 + STARFIELD_NR);

   #declare USE_OBJECT_NUMBER = 44; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mCloudNebula(1,rShape,rColor) rotate V_Rotation translate<0, 0, 0> }

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  dense cloud nebula 43
#if (STARFIELD_SCENE_NR = 21)
   #declare STARFIELD_NR = frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (1825 + STARFIELD_NR);
   #declare NEBULA_COLORS = array[2];
   #declare NEBULA_COLORS[0] = color rgb <RRand(0.5,1.0,rColor), RRand(0.0,0.5,rColor), RRand(0.0,0.5,rColor)>;
   #declare NEBULA_COLORS[1] = color rgb <RRand(0.5,1.0,rColor), RRand(0.5,1.0,rColor), RRand(0.0,0.1,rColor)>;

   #declare USE_OBJECT_NUMBER = 43; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mCloudNebula(NEBULA_COLORS,rShape,rColor) rotate V_Rotation translate<0, 0, 0> }

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  dense cloud nebula 41 & 42
#if (STARFIELD_SCENE_NR = 20)
   #declare STARFIELD_NR = frame_number;
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (1825 + STARFIELD_NR);
   #declare NEBULA_COLORS = array[2];
   #declare NEBULA_COLORS[0] = color rgb <RRand(0.5,1.0,rColor), RRand(0.0,0.5,rColor), RRand(0.0,0.5,rColor)>;
   #declare NEBULA_COLORS[1] = color rgb <RRand(0.5,1.0,rColor), RRand(0.5,1.0,rColor), RRand(0.0,0.1,rColor)>;

   //#declare USE_OBJECT_NUMBER = 41; #include "starfield.inc"
   //#declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   //object { mCloudNebula(NEBULA_COLORS,rShape) rotate V_Rotation translate<-1, 0, 100> }

   #declare USE_OBJECT_NUMBER = 42; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mCloudNebula(NEBULA_COLORS,rShape,rColor) rotate V_Rotation translate<0, 0, 0> }

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }
#end //SCENE

//  dense cloud nebula 41
#if (STARFIELD_SCENE_NR = 19)
   #declare rPosition = seed (6741 + STARFIELD_NR);
   #declare rColor = seed (1825 + STARFIELD_NR);
   #declare NEBULA_COLORS = array[2];
   #declare NEBULA_COLORS[0] = color rgb <RRand(0.5,1.0,rColor), RRand(0.0,0.5,rColor), RRand(0.0,0.5,rColor)>;
   #declare NEBULA_COLORS[1] = color rgb <RRand(0.5,1.0,rColor), RRand(0.0,0.5,rColor), RRand(0.0,0.5,rColor)>;

   #declare USE_OBJECT_NUMBER = 41; #include "starfield.inc"
   #declare V_Rotation = <RRand(-180,180,rPosition),RRand(-180,180,rPosition),RRand(-180,180,rPosition)>;
   object { mCloudNebula(NEBULA_COLORS,rShape,rColor) rotate V_Rotation translate<0, 0, 0> }

   #declare USE_OBJECT_NUMBER = 5; #include "starfield.inc"
   sky_sphere { pigment { P_StarField05 } }

#end //SCENE

// background star concentration
#if (STARFIELD_SCENE_NR = 18)
   #declare starfield_seed_no = 1647286+STARFIELD_NR;
   #declare SeedS = seed(starfield_seed_no);

   //background star concentration
   #declare STARFIELDS_NO = 5; #declare max_star_size = 3;
   #declare iStarfield=1; #while (iStarfield<=STARFIELDS_NO)
      #declare iStartieldType = mod(iStarfield-1,max_star_size)+1; //range [1-4] 
      #declare starfield_star_intensity = RRand(20.0,30.0,SeedS)/iStartieldType; //maximum intensity
      #declare starfield_star_color = rgb<0.7,0.7,1.0>;
      #declare starfield_star_aura = rgb<0.7,0.7,1.0>;
      #declare starfield_seed_no = starfield_seed_no + iStarfield;
      #declare starcluster_excentricity = <10,0.1,1>;
      #declare starcluster_rotation = <0,0,-20>;
      #if(render_quality)
         #declare starfield_star_amount = 10000/pow(iStartieldType,max_star_size);
         #else #declare starfield_star_amount = 1000; #end
      #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
      #declare USE_OBJECT_NUMBER = 16;
      #include "starfield.inc"
      object {O_StarCluster06 rotate <RRand(3,10,SeedS),RRand(3,10,SeedS),RRand(3,10,SeedS)> }
   #declare iStarfield=iStarfield+1; #end
   //plain background
   #declare STARFIELDS_NO = 5; #declare max_star_size = 2;
   #declare iStarfield=1; #while (iStarfield<=STARFIELDS_NO)
      #declare iStartieldType = mod(iStarfield-1,max_star_size)+1; //range [1-4] 
      #declare starfield_star_intensity = RRand(10.0,30.0,SeedS)/iStartieldType; //maximum intensity
      #declare starfield_star_color = rgb<0.7,0.7,1.0>;
      #declare starfield_star_aura = rgb<0.7,0.7,1.0>;
      #declare starfield_seed_no = starfield_seed_no + iStarfield;
      #declare starcluster_excentricity = <1,1,1>;
      #declare starcluster_rotation = <30,30,30>;
      #if(render_quality)
         #declare starfield_star_amount = 10000/pow(iStartieldType,max_star_size);
         #else #declare starfield_star_amount = 1000; #end
      #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
      #declare USE_OBJECT_NUMBER = 14;
      #include "starfield.inc"
      object {O_StarCluster04 } //rotate <RRand(3,10,SeedS),RRand(3,10,SeedS),RRand(3,10,SeedS)> }
   #declare iStarfield=iStarfield+1; #end
#end //SCENE

// triangle based globular cluster - EXPERIMENTAL
#if (STARFIELD_SCENE_NR = 17)
   #declare starfield_seed_no = 1647286+STARFIELD_NR;
   #declare SeedS = seed(starfield_seed_no);

   //globular nebula
   #declare STARFIELDS_NO = 5; //IRand(2,5,SeedS);
   #declare STARFIELD=1;   
   #while (STARFIELD<=STARFIELDS_NO)
      //#declare iStartieldType = IRand(1,2,SeedS);      
      #if (STARFIELD=1) #declare iStartieldType = 1; #else #declare iStartieldType = 2; #end     
      #declare starfield_star_intensity = 0.5*RRand(3.0,5.0,SeedS); //maximum intensity
      #declare starfield_star_color = rgb <1,1,1>; //rgb <RRand(0.95,1.0,SeedS), RRand(0.95,1.0,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_star_aura = rgb<0.7,0.7,1.0>; //rgb <RRand(0.9,0.99,SeedS), RRand(0.9,0.99,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_seed_no = starfield_seed_no + STARFIELD;
      #declare starcluster_excentricity = <1,1,1>; //<RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <0,0,0>; //<RRand(10,180,SeedS), RRand(10,180,SeedS), RRand(10,180,SeedS)>;
      #declare starfield_distribu_angle = 2.0; //RRand(1,10,SeedS); // defines the radius of a globular cluster
      #if(render_quality) #declare starfield_star_amount = 2000*starfield_distribu_angle/pow(iStartieldType,2); #else #declare starfield_star_amount = 100; #end
      #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
      #declare USE_OBJECT_NUMBER = 13;
      #include "starfield.inc"
      object {O_StarCluster03}
   #declare STARFIELD=STARFIELD+1; #end
   //tubular nebula
   #declare STARFIELDS_NO = 5; //IRand(2,5,SeedS);
   #declare STARFIELD=1;   
   #while (STARFIELD<=STARFIELDS_NO)
      //#declare iStartieldType = IRand(1,2,SeedS);      
      #if (STARFIELD=1) #declare iStartieldType = 1; #else #declare iStartieldType = 2; #end     
      #declare starfield_star_intensity = 0.5*RRand(2.0,3.0,SeedS); //maximum intensity
      #declare starfield_star_color = rgb <1,1,1>; //rgb <RRand(0.95,1.0,SeedS), RRand(0.95,1.0,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_star_aura = rgb<0.7,0.7,1.0>; //rgb <RRand(0.9,0.99,SeedS), RRand(0.9,0.99,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_seed_no = starfield_seed_no + STARFIELD;
      #declare starcluster_excentricity = <0.01,5,0.01>; //<RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <0,0,30>; //<RRand(10,180,SeedS), RRand(10,180,SeedS), RRand(10,180,SeedS)>;
      #declare starfield_distribu_angle = 1.5; //RRand(1,10,SeedS); // defines the radius of a globular cluster
      #if(render_quality) #declare starfield_star_amount = 1000*starfield_distribu_angle/pow(iStartieldType,2); #else #declare starfield_star_amount = 100; #end
      #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
      #declare USE_OBJECT_NUMBER = 13;
      #include "starfield.inc"
      object {O_StarCluster03}
   #declare STARFIELD=STARFIELD+1; #end
#end

// sphere based globular cluster
#if (STARFIELD_SCENE_NR = 16)
   #declare starfield_seed_no = 1647286+STARFIELD_NR;
   #declare SeedS = seed(starfield_seed_no);

   //globular nebula
   #declare STARFIELDS_NO = 5; //IRand(2,5,SeedS);
   #declare STARFIELD=1;   
   #while (STARFIELD<=STARFIELDS_NO)
      //#declare iStartieldType = IRand(1,2,SeedS);      
      #if (STARFIELD=1) #declare iStartieldType = 1; #else #declare iStartieldType = 2; #end     
      #declare starfield_star_intensity = RRand(3.0,5.0,SeedS); //maximum intensity
      #declare starfield_star_color = rgb <0.7,0.7,1>; //rgb <RRand(0.95,1.0,SeedS), RRand(0.95,1.0,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_star_aura = rgb<0.7,0.7,1.0>; //rgb <RRand(0.9,0.99,SeedS), RRand(0.9,0.99,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_seed_no = starfield_seed_no + STARFIELD;
      #declare starcluster_excentricity = <1,1,1>; //<RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <0,0,0>; //<RRand(10,180,SeedS), RRand(10,180,SeedS), RRand(10,180,SeedS)>;
      #declare starfield_distribu_angle = 2.0; //RRand(1,10,SeedS); // defines the radius of a globular cluster
      #if(render_quality) #declare starfield_star_amount = 2000*starfield_distribu_angle/pow(iStartieldType,2); #else #declare starfield_star_amount = 100; #end
      #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
      #declare USE_OBJECT_NUMBER = 16;
      #include "starfield.inc"
      object {O_StarCluster06}
   #declare STARFIELD=STARFIELD+1; #end
   //tubular nebula
   #declare STARFIELDS_NO = 5; //IRand(2,5,SeedS);
   #declare STARFIELD=1;   
   #while (STARFIELD<=STARFIELDS_NO)
      //#declare iStartieldType = IRand(1,2,SeedS);      
      #if (STARFIELD=1) #declare iStartieldType = 1; #else #declare iStartieldType = 2; #end     
      #declare starfield_star_intensity = RRand(2.0,3.0,SeedS); //maximum intensity
      #declare starfield_star_color = rgb <0.7,0.7,1>; //rgb <RRand(0.95,1.0,SeedS), RRand(0.95,1.0,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_star_aura = rgb<0.7,0.7,1.0>; //rgb <RRand(0.9,0.99,SeedS), RRand(0.9,0.99,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_seed_no = starfield_seed_no + STARFIELD;
      #declare starcluster_excentricity = <0.01,5,0.01>; //<RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <0,0,30>; //<RRand(10,180,SeedS), RRand(10,180,SeedS), RRand(10,180,SeedS)>;
      #declare starfield_distribu_angle = 1.5; //RRand(1,10,SeedS); // defines the radius of a globular cluster
      #if(render_quality) #declare starfield_star_amount = 1000*starfield_distribu_angle/pow(iStartieldType,2); #else #declare starfield_star_amount = 100; #end
      #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
      #declare USE_OBJECT_NUMBER = 16;
      #include "starfield.inc"
      object {O_StarCluster06}
   #declare STARFIELD=STARFIELD+1; #end
#end

// multiple triangle based star fields overlayed
#if (STARFIELD_SCENE_NR = 15)

   #declare create_logfile = false;
   #declare starfield_seed_no = 16486+STARFIELD_NR;
   #declare SeedS = seed(starfield_seed_no);

   #declare STARFIELDS_NO = 4; //IRand(2,5,SeedS);
   #declare STARFIELD=1;   
   #while (STARFIELD<=STARFIELDS_NO)
      #declare iStartieldType = STARFIELD; //IRand(2,4,SeedS);      
      #declare starfield_star_intensity = RRand(3.0,5.0,SeedS); //maximum intensity
      #declare starfield_star_color = rgb <0.7,0.7,1>; 
      #declare starfield_star_aura = rgb<0.7,0.7,1.0>; 
      #declare starfield_seed_no = starfield_seed_no + STARFIELD;
      #declare starcluster_excentricity = <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <30,30,30>; //<RRand(10,180,SeedS), RRand(10,180,SeedS), RRand(10,180,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = 100000/pow(iStartieldType,3);
         #else #declare starfield_star_amount = 10000; #end
      #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
      #declare USE_OBJECT_NUMBER = 15;
      #include "starfield.inc"
      object {O_StarCluster05}
   #declare STARFIELD=STARFIELD+1; #end
#end

// triangle based star field and cluster types tests
// run frames 1-5 to see all sizes
// or change STARFIELD_STAR_TYPE to values 1-5 to make tests with parameters
// performance v0.14 (40k stars type 3 1280x1024 AA0.3): 70M tokens, 341s parse time, 17m 54s (til line 150)
// performance v0.15 (40k stars type 3 1280x1024 AA0.3): 10M tokens, 28s parse time, 5m 30s (-"-)
#if (STARFIELD_SCENE_NR = 14)
   #declare create_logfile = false;
   #declare starfield_seed_no = 23241+STARFIELD_NR;
   #declare SeedS = seed(starfield_seed_no);
   #if (frame_number=0) #declare iStartieldType = 3; #else #declare iStartieldType = frame_number; #end

   #declare starfield_star_intensity = 3; //maximum intensity
   #declare starfield_star_color = rgb <0.7, 0.7, 1>;
   #declare starfield_star_aura = rgb <0.7,0.7,1.0>; //rgb <RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS)>;
   #declare starfield_seed_no = starfield_seed_no + iStartieldType;
   #declare starcluster_excentricity = <1.0, 1.5, 1>; //<RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
   #declare starcluster_rotation = <30,30,30>; //<180,180,180>; //<RRand(0,180,SeedS), RRand(0,180,SeedS), RRand(0,180,SeedS)>;
   #if(render_quality) #declare starfield_star_amount = 5000/pow(iStartieldType,2); #else #declare starfield_star_amount = 40000; #end
   #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
   #declare USE_OBJECT_NUMBER = 15;
   #include "starfield.inc"
   object {O_StarCluster05}
#end

// sphere based star field and cluster types tests
// run frames 1-5 to see all sizes
// or change STARFIELD_STAR_TYPE to values 1-5 to make tests with parameters
// performance v0.14 (40k stars type 3 1280x1024 AA0.3): 70M tokens, 373s parse time, 11m 28s (til line 150)
// performance v0.15 (40k stars type 3 1280x1024 AA0.3): 10M tokens, 334s parse time, 11m 30s (-"-)
// max objects: 300k stars type 2 1024x768 AA0.3 
#if (STARFIELD_SCENE_NR = 13)

   #declare create_logfile = false;
   #declare starfield_seed_no = 7654321+STARFIELD_NR;
   #declare SeedS = seed(starfield_seed_no);
   #if (frame_number=0) #declare iStartieldType = 2; #else #declare iStartieldType = frame_number; #end

   #declare starfield_star_intensity = 5; //maximum intensity
   #declare starfield_star_color = rgb <1, 1, 1>;
   #declare starfield_star_aura = rgb <0.7,0.7,1.0>; //rgb <RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS)>;
   #declare starfield_seed_no = starfield_seed_no + iStartieldType;
   #declare starcluster_excentricity = <1.0, 1.5, 1>; //<RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
   #declare starcluster_rotation = <30,30,30>; //<180,180,180>; //<RRand(0,180,SeedS), RRand(0,180,SeedS), RRand(0,180,SeedS)>;
   #if(render_quality) #declare starfield_star_amount = 5000/pow(iStartieldType,2); #else #declare starfield_star_amount = 400000; #end
   #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
      #declare USE_OBJECT_NUMBER = 14;
   #include "starfield.inc"
   object {O_StarCluster04}

#end

// multiple sphere based star fields overlayed
#if (STARFIELD_SCENE_NR = 12)

   #declare create_logfile = false;
   #declare starfield_seed_no = 16486+STARFIELD_NR;
   #declare SeedS = seed(starfield_seed_no);

   #declare STARFIELDS_NO = 4; //IRand(2,5,SeedS);
   #declare STARFIELD=1;   
   #while (STARFIELD<=STARFIELDS_NO)
      #declare iStartieldType = STARFIELD; //IRand(1,3,SeedS);      
      #declare starfield_star_intensity = RRand(3.0,5.0,SeedS); //maximum intensity
      #declare starfield_star_color = rgb <1,1,1>; //rgb <RRand(0.95,1.0,SeedS), RRand(0.95,1.0,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_star_aura = rgb<0.7,0.7,1.0>; //rgb <RRand(0.9,0.99,SeedS), RRand(0.9,0.99,SeedS), RRand(0.99,1.0,SeedS)>;
      #declare starfield_seed_no = starfield_seed_no + STARFIELD;
      #declare starcluster_excentricity = <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <30,30,30>; //<RRand(10,180,SeedS), RRand(10,180,SeedS), RRand(10,180,SeedS)>;
      #if(render_quality)
         //#declare starfield_star_amount = 0.05*(starcluster_rotation.x+starcluster_rotation.y+starcluster_rotation.z)*5000/pow(iStartieldType,5);
         #declare starfield_star_amount = 10000/pow(iStartieldType,3);
      #else #declare starfield_star_amount = 1000; #end
      #declare STARFIELD_STAR_TYPE = iStartieldType; //1=tiny; 2=small; 3=medium; 4=big; 5=large
      #declare USE_OBJECT_NUMBER = 14;
      #include "starfield.inc"
      object {O_StarCluster04}
   #declare STARFIELD=STARFIELD+1; #end

#end

// random starfield, star nebula, cloud nebula, and star cluster
#if (STARFIELD_SCENE_NR = 11)

   #declare SeedS = seed(92118+STARFIELD_NR);
   #declare STARFIELDS_NO = IRand(0,2,SeedS);
   #declare STARNEBULA_NO = IRand(0,2,SeedS);
   #declare CLOUDNEBULA_NO = IRand(0,2,SeedS);
   #declare P_StarField = array[STARFIELDS_NO+1];
   #declare P_StarNebula = array[STARNEBULA_NO+1];
   #declare P_CloudNebula = array[CLOUDNEBULA_NO+1];

   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_skysphere_no = 0;
      #declare starfield_star_intensity = RRand(1.0,1.2,SeedS);
      #declare starfield_star_color = rgb <RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS)>;
      #include "starfield.inc"
      //#debug concat("I=",str(I,0,0),"\n")
      #declare SF_NUMBER = IRand(1,5,SeedS);
      #switch (SF_NUMBER)
         #case(1) #declare SF = P_StarField01; #break
         #case(2) #declare SF = P_StarField02; #break
         #case(3) #declare SF = P_StarField03; #break
         #case(4) #declare SF = P_StarField04; #break
         #case(5) #declare SF = P_StarField05; #break
      #end
      #declare P_StarField[I] = SF;
   #declare I=I+1; #end

   #declare I=1;   
   #while (I<=STARNEBULA_NO)
      #declare starfield_skysphere_no = 0;
      #declare starfield_star_intensity = RRand(1.0,1.5,SeedS);
      #declare starfield_star_color = rgb <RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS)>;
      #declare starfield_star_aura = rgb <RRand(0.2,1.0,SeedS), RRand(0.2,1.0,SeedS), RRand(0.2,1.0,SeedS)>;
      #declare starcluster_excentricity = <RRand(1.0,10.0,SeedS), RRand(1.0,10.0,SeedS), RRand(1.0,10.0,SeedS)>;
      #declare starcluster_rotation = <RRand(0,30,SeedS), RRand(0,30,SeedS), RRand(-90,90,SeedS)>;
      #include "starfield.inc"
      //#debug concat("I=",str(I,0,0),"\n")
      #declare SF_NUMBER = IRand(1,4,SeedS);
      #switch (SF_NUMBER)
         #case(1) #declare SF = P_StarNebula01; #break
         #case(2) #declare SF = P_StarNebula02; #break
         #case(3) #declare SF = P_StarNebula03; #break
         #case(4) #declare SF = P_StarNebula04; #break
      #end
      #declare P_StarNebula[I] = SF;
   #declare I=I+1; #end

   #declare I=1;   
   #while (I<=CLOUDNEBULA_NO)
      #declare starfield_skysphere_no = 0;
      #declare starfield_star_intensity = RRand(1.0,1.3,SeedS);
      #declare starfield_star_color = rgb <0, 0, 0>;
      #declare starfield_star_aura = rgb <RRand(0.2,1.0,SeedS), RRand(0.2,1.0,SeedS), RRand(0.2,1.0,SeedS)>;
      #declare starcluster_excentricity = <RRand(1.0,5.0,SeedS), RRand(1.0,5.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <RRand(0,90,SeedS), RRand(0,90,SeedS), RRand(-90,90,SeedS)>;
      #include "starfield.inc"
      //#debug concat("I=",str(I,0,0),"\n")
      #declare SF_NUMBER = IRand(1,4,SeedS);
      #switch (SF_NUMBER)
         #case(1) #declare SF = P_CloudNebula01; #break
         #case(2) #declare SF = P_CloudNebula02; #break
         #case(3) #declare SF = P_CloudNebula03; #break
         #case(4) #declare SF = P_CloudNebula04; #break
      #end
      #declare P_CloudNebula[I] = SF;
   #declare I=I+1; #end

   // starfield concentrations
   #declare starfield_skysphere_no = 0;
   #declare starfield_star_intensity = RRand(1.0,1.1,SeedS);
   #declare starfield_star_color = rgb <RRand(0.5,1.0,SeedS), RRand(0.5,1.0,SeedS), RRand(0.5,1.0,SeedS)>;
   #declare starfield_star_aura = rgb <0.0, 0.0, 0.0>;
   #declare starcluster_excentricity = <RRand(0.5,2.0,SeedS), RRand(0.5,2.0,SeedS), RRand(0.5,2.0,SeedS)>;
   #declare starcluster_rotation = <RRand(0,90,SeedS), RRand(0,90,SeedS), RRand(-90,90,SeedS)>;
   #include "starfield.inc"
      #declare SF_NUMBER = IRand(1,2,SeedS);
      #switch (SF_NUMBER)
         #case(1) #declare SF = P_StarNebula01; #break
         #case(2) #declare SF = P_StarNebula04; #break
      #end
   #declare P_StarConcentration = SF;

   #declare O_StarField = sky_sphere {
      #declare I=1; #while (I<=STARFIELDS_NO)
         pigment { P_StarField[I] }
      #declare I=I+1; #end
      #declare I=1; #while (I<=STARNEBULA_NO)
         pigment { P_StarNebula[I] }
      #declare I=I+1; #end
      #declare I=1; #while (I<=CLOUDNEBULA_NO)
         pigment { P_CloudNebula[I] }
      #declare I=I+1; #end
      pigment { P_StarConcentration }
   }
   sky_sphere {O_StarField}

   //starfield with normal stars   
   #declare STARFIELDS_NO = IRand(2,6,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(1.0,1.2,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.5,1.0,SeedS), RRand(0.5,1.0,SeedS), RRand(0.5,1.0,SeedS)>;
      #declare starfield_seed_no = 8234594 + frame_number + I;
      #declare starfield_starsize_min = RRand(0.1,0.5,SeedS);
      #declare starfield_starsize_max = RRand(0.5,1.5,SeedS);
      #declare starfield_distribu_angle = RRand(20,50,SeedS);
      #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
      #declare starcluster_rotation = <RRand(0,90,SeedS), RRand(0,90,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(100,255,SeedS); #else #declare starfield_star_amount = 100; #end
      #include "starfield.inc"
      object {O_StarCluster02}
   #declare I=I+1; #end

   //big stars   
   #declare STARFIELDS_NO = IRand(4,20,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(1.5,2.0,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS)>;
      #declare starfield_seed_no = 3234548 + frame_number + I;
      #declare starfield_starsize_min = RRand(0.5,2.0,SeedS);
      #declare starfield_starsize_max = RRand(2.0,4.0,SeedS);
      #declare starfield_distribu_angle = RRand(30,90,SeedS);
      #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
      #declare starcluster_rotation = <RRand(0,90,SeedS), RRand(0,90,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(10,100,SeedS); #else #declare starfield_star_amount = 50; #end
      #include "starfield.inc"
      object {O_StarCluster02}
   #declare I=I+1; #end

   //huge stars   
   #declare STARFIELDS_NO = IRand(1,4,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(1.5,2.0,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS)>;
      #declare starfield_seed_no = 9234872 + frame_number + I;
      #declare starfield_starsize_min = RRand(2.0,5.0,SeedS);
      #declare starfield_starsize_max = RRand(5.0,20.0,SeedS);
      #declare starfield_distribu_angle = RRand(30,90,SeedS);
      #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
      #declare starcluster_rotation = <RRand(0,30,SeedS), RRand(0,30,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(2,10,SeedS); #else #declare starfield_star_amount = 10; #end
      #include "starfield.inc"
      object {O_StarCluster02}
   #declare I=I+1; #end

   // star clusters
   #declare STARFIELDS_NO = IRand(0,1,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(1.0,1.5,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS)>;
      #declare starfield_seed_no = 1938524 + frame_number + I;
      #declare starfield_starsize_min = RRand(1.0,2.0,SeedS);
      #declare starfield_starsize_max = RRand(2.0,3.0,SeedS);
      #declare starfield_distribu_angle = RRand(1,6,SeedS);
      #declare starcluster_excentricity = <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <RRand(0,90,SeedS), RRand(0,90,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(100,255,SeedS); #else #declare starfield_star_amount = 100; #end
      #include "starfield.inc"
      object {O_StarCluster03}
   #declare I=I+1; #end

#end

// random starfield, star nebula, cloud nebula, and star cluster
#if (STARFIELD_SCENE_NR = 10)

   #declare SeedS = seed(1230211+STARFIELD_NR);
   #declare STARFIELDS_NO = IRand(2,4,SeedS);
   #declare STARNEBULA_NO = IRand(1,3,SeedS);
   #declare CLOUDNEBULA_NO = IRand(1,2,SeedS);
   #declare P_StarField = array[STARFIELDS_NO+1];
   #declare P_StarNebula = array[STARNEBULA_NO+1];
   #declare P_CloudNebula = array[CLOUDNEBULA_NO+1];

   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_skysphere_no = 0;
      #declare starfield_star_intensity = RRand(1.0,1.2,SeedS);
      #declare starfield_star_color = rgb <RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS)>;
      #include "starfield.inc"
      //#debug concat("I=",str(I,0,0),"\n")
      #declare SF_NUMBER = IRand(1,5,SeedS);
      #switch (SF_NUMBER)
         #case(1) #declare SF = P_StarField01; #break
         #case(2) #declare SF = P_StarField02; #break
         #case(3) #declare SF = P_StarField03; #break
         #case(4) #declare SF = P_StarField04; #break
         #case(5) #declare SF = P_StarField05; #break
      #end
      #declare P_StarField[I] = SF;
   #declare I=I+1; #end

   #declare I=1;   
   #while (I<=STARNEBULA_NO)
      #declare starfield_skysphere_no = 0;
      #declare starfield_star_intensity = RRand(1.0,1.5,SeedS);
      #declare starfield_star_color = rgb <RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS)>;
      #declare starfield_star_aura = rgb <RRand(0.2,1.0,SeedS), RRand(0.2,1.0,SeedS), RRand(0.2,1.0,SeedS)>;
      #declare starcluster_excentricity = <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <RRand(0,30,SeedS), RRand(0,30,SeedS), RRand(-90,90,SeedS)>;
      #include "starfield.inc"
      //#debug concat("I=",str(I,0,0),"\n")
      #declare SF_NUMBER = IRand(1,4,SeedS);
      #switch (SF_NUMBER)
         #case(1) #declare SF = P_StarNebula01; #break
         #case(2) #declare SF = P_StarNebula02; #break
         #case(3) #declare SF = P_StarNebula03; #break
         #case(4) #declare SF = P_StarNebula04; #break
      #end
      #declare P_StarNebula[I] = SF;
   #declare I=I+1; #end

   #declare I=1;   
   #while (I<=CLOUDNEBULA_NO)
      #declare starfield_skysphere_no = 0;
      #declare starfield_star_intensity = RRand(1.0,1.3,SeedS);
      #declare starfield_star_color = rgb <RRand(0.0,1.0,SeedS), RRand(0.0,1.0,SeedS), RRand(0.0,1.0,SeedS)>;
      #declare starfield_star_aura = rgb <RRand(0.2,1.0,SeedS), RRand(0.2,1.0,SeedS), RRand(0.2,1.0,SeedS)>;
      #declare starcluster_excentricity = <RRand(1.0,5.0,SeedS), RRand(1.0,5.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <RRand(0,90,SeedS), RRand(0,90,SeedS), RRand(-90,90,SeedS)>;
      #include "starfield.inc"
      //#debug concat("I=",str(I,0,0),"\n")
      #declare SF_NUMBER = IRand(1,4,SeedS);
      #switch (SF_NUMBER)
         #case(1) #declare SF = P_CloudNebula01; #break
         #case(2) #declare SF = P_CloudNebula02; #break
         #case(3) #declare SF = P_CloudNebula03; #break
         #case(4) #declare SF = P_CloudNebula04; #break
      #end
      #declare P_CloudNebula[I] = SF;
   #declare I=I+1; #end

   #declare O_StarField = sky_sphere {
      #declare I=1; #while (I<=STARFIELDS_NO)
         pigment { P_StarField[I] }
      #declare I=I+1; #end
      #declare I=1; #while (I<=STARNEBULA_NO)
         pigment { P_StarNebula[I] }
      #declare I=I+1; #end
      #declare I=1; #while (I<=CLOUDNEBULA_NO)
         pigment { P_CloudNebula[I] }
      #declare I=I+1; #end
   }
   sky_sphere {O_StarField}

   //starfield with normal stars   
   #declare STARFIELDS_NO = IRand(2,6,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(1.0,1.2,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.5,1.0,SeedS), RRand(0.5,1.0,SeedS), RRand(0.5,1.0,SeedS)>;
      #declare starfield_seed_no = 3234594 + frame_number + I;
      #declare starfield_starsize_min = RRand(0.1,0.5,SeedS);
      #declare starfield_starsize_max = RRand(0.5,1.5,SeedS);
      #declare starfield_distribu_angle = RRand(20,50,SeedS);
      #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
      #declare starcluster_rotation = <RRand(0,10,SeedS), RRand(0,10,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(100,255,SeedS); #else #declare starfield_star_amount = 100; #end
      #include "starfield.inc"
      object {O_StarCluster02}
   #declare I=I+1; #end

   //big stars   
   #declare STARFIELDS_NO = IRand(4,20,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(1.5,2.0,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS)>;
      #declare starfield_seed_no = 3234542 + frame_number + I;
      #declare starfield_starsize_min = RRand(0.5,2.0,SeedS);
      #declare starfield_starsize_max = RRand(2.0,4.0,SeedS);
      #declare starfield_distribu_angle = RRand(30,90,SeedS);
      #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
      #declare starcluster_rotation = <RRand(0,10,SeedS), RRand(0,10,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(10,100,SeedS); #else #declare starfield_star_amount = 50; #end
      #include "starfield.inc"
      object {O_StarCluster02}
   #declare I=I+1; #end

   //huge stars   
   #declare STARFIELDS_NO = IRand(1,4,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(1.5,2.0,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS)>;
      #declare starfield_seed_no = 3234572 + frame_number + I;
      #declare starfield_starsize_min = RRand(2.0,4.0,SeedS);
      #declare starfield_starsize_max = RRand(4.0,10.0,SeedS);
      #declare starfield_distribu_angle = RRand(30,90,SeedS);
      #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
      #declare starcluster_rotation = <RRand(0,10,SeedS), RRand(0,10,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(2,50,SeedS); #else #declare starfield_star_amount = 10; #end
      #include "starfield.inc"
      object {O_StarCluster02}
   #declare I=I+1; #end

   // star clusters
   #declare STARFIELDS_NO = IRand(0,1,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(1.0,1.5,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS)>;
      #declare starfield_seed_no = 1138524 + frame_number + I;
      #declare starfield_starsize_min = RRand(1.0,2.0,SeedS);
      #declare starfield_starsize_max = RRand(2.0,3.0,SeedS);
      #declare starfield_distribu_angle = RRand(1,6,SeedS);
      #declare starcluster_excentricity = <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <RRand(0,90,SeedS), RRand(0,90,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(100,255,SeedS); #else #declare starfield_star_amount = 100; #end
      #include "starfield.inc"
      object {O_StarCluster03}
   #declare I=I+1; #end

#end

// random starfield background with nebula and cluster
#if (STARFIELD_SCENE_NR = 9)

   #declare SeedS = seed(1+STARFIELD_NR);
   #declare STARFIELDS_NO = IRand(1,3,SeedS);
   #declare STARNEBULA_NO = IRand(1,2,SeedS);
   #declare P_StarField = array[STARFIELDS_NO+1];
   #declare P_StarNebula = array[STARNEBULA_NO+1];

   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_skysphere_no = 0;
      #declare starfield_star_intensity = 1.0;
      #declare starfield_star_color = rgb <RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS)>;
      #include "starfield.inc"
      //#debug concat("I=",str(I,0,0),"\n")
      #declare SF_NUMBER = IRand(1,5,SeedS);
      #switch (SF_NUMBER)
         #case(1) #declare SF = P_StarField01; #break
         #case(2) #declare SF = P_StarField02; #break
         #case(3) #declare SF = P_StarField03; #break
         #case(4) #declare SF = P_StarField04; #break
         #case(5) #declare SF = P_StarField05; #break
      #end
      #declare P_StarField[I] = SF;
   #declare I=I+1; #end

   #declare I=1;   
   #while (I<=STARNEBULA_NO)
      #declare starfield_skysphere_no = 0;
      #declare starfield_star_intensity = 1.0;
      #declare starfield_star_color = rgb <RRand(0.0,1.0,SeedS), RRand(0.0,1.0,SeedS), RRand(0.0,1.0,SeedS)>;
      #declare starfield_star_aura = rgb <RRand(0.0,1.0,SeedS), RRand(0.0,1.0,SeedS), RRand(0.0,1.0,SeedS)>;
      #declare starcluster_excentricity = <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <RRand(0,30,SeedS), RRand(0,30,SeedS), RRand(-90,90,SeedS)>;
      #include "starfield.inc"
      //#debug concat("I=",str(I,0,0),"\n")
      #declare SF_NUMBER = IRand(1,4,SeedS);
      #switch (SF_NUMBER)
         #case(1) #declare SF = P_StarNebula01; #break
         #case(2) #declare SF = P_StarNebula02; #break
         #case(3) #declare SF = P_StarNebula03; #break
         #case(4) #declare SF = P_StarNebula04; #break
      #end
      #declare P_StarNebula[I] = SF;
   #declare I=I+1; #end

   #declare O_StarField = sky_sphere {
      #declare I=1; #while (I<=STARFIELDS_NO)
         pigment { P_StarField[I] }
      #declare I=I+1; #end
      #declare I=1; #while (I<=STARNEBULA_NO)
         pigment { P_StarNebula[I] }
      #declare I=I+1; #end
   }
   sky_sphere {O_StarField}

   //starfield with big stars   
   #declare STARFIELDS_NO = IRand(2,6,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(0.9,1.2,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS)>;
      #declare starfield_seed_no = 1234544 + frame_number + I;
      #declare starfield_starsize_min = RRand(0.1,0.5,SeedS);
      #declare starfield_starsize_max = RRand(0.5,1.5,SeedS);
      #declare starfield_distribu_angle = RRand(20,50,SeedS);
      #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
      #declare starcluster_rotation = <RRand(0,10,SeedS), RRand(0,10,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(100,255,SeedS); #else #declare starfield_star_amount = 100; #end
      #include "starfield.inc"
      object {O_StarCluster02}
   #declare I=I+1; #end

   //huge stars   
   #declare STARFIELDS_NO = IRand(4,20,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(1.5,2.0,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS)>;
      #declare starfield_seed_no = 1234512 + frame_number + I;
      #declare starfield_starsize_min = RRand(1.0,2.0,SeedS);
      #declare starfield_starsize_max = RRand(2.0,4.0,SeedS);
      #declare starfield_distribu_angle = RRand(30,90,SeedS);
      #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
      #declare starcluster_rotation = <RRand(0,10,SeedS), RRand(0,10,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(100,255,SeedS); #else #declare starfield_star_amount = 100; #end
      #include "starfield.inc"
      object {O_StarCluster02}
   #declare I=I+1; #end

   // star clusters
   #declare STARFIELDS_NO = IRand(1,2,SeedS);
   #declare I=1;   
   #while (I<=STARFIELDS_NO)
      #declare starfield_star_intensity = RRand(0.9,1.5,SeedS);
      #declare starfield_star_color = rgb <1, 1, 1>;
      #declare starfield_star_aura = rgb <RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS), RRand(0.8,1.0,SeedS)>;
      #declare starfield_seed_no = 518514 + frame_number + I;
      #declare starfield_starsize_min = RRand(0.5,1.0,SeedS);
      #declare starfield_starsize_max = RRand(1.0,4.0,SeedS);
      #declare starfield_distribu_angle = RRand(1,6,SeedS);
      #declare starcluster_excentricity = <RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS), RRand(1.0,2.0,SeedS)>;
      #declare starcluster_rotation = <RRand(0,30,SeedS), RRand(0,30,SeedS), RRand(-90,90,SeedS)>;
      #if(render_quality) #declare starfield_star_amount = IRand(100,255,SeedS); #else #declare starfield_star_amount = 100; #end
      #include "starfield.inc"
      object {O_StarCluster02}
   #declare I=I+1; #end

#end

#if (STARFIELD_SCENE_NR = 8)

   #declare SeedS = seed(frame_number+1);

   #declare starfield_skysphere_no = 0;
   #declare starfield_star_intensity = 1.1;
   #declare starfield_star_color = rgb <0.8, 0.9, 1.0>;
   #declare starfield_star_aura = rgb <0.0, 0.0, 0.0>;
   #declare starcluster_excentricity = <5.0, 1.0, 1.0>;
   //#declare starfield_star_aura = rgb <0.4, 0.6, 0.9>;
   //#declare starcluster_rotation = <RRand(0,50,SeedS), RRand(0,50,SeedS), RRand(-90,90,SeedS)>;
   #declare starcluster_rotation = <-30, -30, 0>;
   #include "starfield.inc"
   #declare O_StarField = sky_sphere {
      //pigment { P_StarField05 rotate starcluster_rotation }
      pigment { P_StarNebula04 rotate starcluster_rotation }
      //pigment { P_CloudNebula01 rotate starcluster_rotation }
      //pigment { P_CloudNebula02 }
      //pigment { P_CloudNebula03 }
      //pigment { P_CloudNebula04 }
   }
   sky_sphere {O_StarField}

/*
   #declare starfield_skysphere_no = 0;
   #declare starfield_star_intensity = 1.0; //RRand(1.5,2.0,SeedS);
   #declare starfield_star_color = rgb <1, 1, 1>;
   #declare starfield_star_aura = rgb <0.6, 0.75, 1.0>;
   #declare starfield_seed_no = 1234711;
   #declare starfield_starsize_min = 1; //RRand(1.0,2.0,SeedS);
   #declare starfield_starsize_max = 5; //RRand(2.0,4.0,SeedS);
   #declare starfield_distribu_angle = 5; //RRand(30,90,SeedS);
   #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
   //#declare starcluster_rotation = <RRand(0,10,SeedS), RRand(0,10,SeedS), RRand(-90,90,SeedS)>;
   #declare starcluster_rotation = <-10, -5, 0>;
   #declare starfield_star_amount = 1000; //IRand(10,100,SeedS);
   #include "starfield.inc"
   object {O_StarCluster03}
*/

#end

#if (STARFIELD_SCENE_NR = 7)

   #declare SeedS = seed(frame_number+1);

   #declare starfield_skysphere_no = 0;
   #declare starfield_star_intensity = 1.0;
   #declare starfield_star_color = rgb <0.8, 0.9, 1.0>;
   #include "starfield.inc"
   #declare O_StarField = sky_sphere {
      pigment { P_StarField05 rotate starcluster_rotation }
   }
   sky_sphere {O_StarField}

   #declare starfield_skysphere_no = 0;
   #declare starfield_star_intensity = 1.0; //RRand(1.5,2.0,SeedS);
   #declare starfield_star_color = rgb <1, 1, 1>;
   //#declare starfield_star_aura = rgb <RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS), RRand(0.7,1.0,SeedS)>;
   #declare starfield_star_aura = rgb <0.6, 0.75, 1.0>;
   #declare starfield_seed_no = 12347;
   #declare starfield_starsize_min = 2; //RRand(1.0,2.0,SeedS);
   #declare starfield_starsize_max = 10; //RRand(2.0,4.0,SeedS);
   #declare starfield_distribu_angle = RRand(30,90,SeedS);
   #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
   #declare starcluster_rotation = <RRand(0,10,SeedS), RRand(0,10,SeedS), RRand(-90,90,SeedS)>;
   #declare starfield_star_amount = IRand(10,100,SeedS);
   #include "starfield.inc"
   object {O_StarCluster02}

#end

#if (STARFIELD_SCENE_NR = 6)

   #declare starfield_skysphere_no = 0;
   #declare starfield_star_intensity = 1.0;
   #declare starfield_star_color = rgb <0.8, 0.9, 1.0>;
   #include "starfield.inc"

   #declare O_StarField = sky_sphere {
      pigment { P_StarField05 rotate starcluster_rotation }
      pigment { P_StarNebula04 rotate starcluster_rotation }
   }
   sky_sphere {O_StarField}
   
   #declare starfield_star_intensity = 1.0;
   #declare starfield_star_color = rgb <1, 1, 1>;
   #declare starfield_star_aura = rgb <0.6, 0.75, 1.0>;
   //declare starfield_star_aura = rgb <0.9, 0.6, 0.5>;
   #declare starcluster_rotation = <90, 0, -45>;
   #declare starfield_seed_no = 1234567 + frame_number;
   #declare starfield_starsize_min = 0.1;
   #declare starfield_starsize_max = 1.0;
   #declare starfield_distribu_angle = 60;
   #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
   #declare starcluster_rotation = <0, 0, 0>;
   #if(render_quality) #declare starfield_star_amount = 1000; #else #declare starfield_star_amount = 100; #end
   #include "starfield.inc"
   object {O_StarCluster01}

   #declare starfield_star_intensity = 1.0;
   #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
   #declare starfield_star_aura = rgb <0.6, 0.75, 1.0>;
   //declare starfield_star_aura = rgb <0.9, 0.6, 0.5>;
   #declare starcluster_rotation = <90, 0, -45>;
   #declare starfield_seed_no = 1234567 + frame_number;
   #declare starfield_starsize_min = 0.1;
   #declare starfield_starsize_max = 2.0;
   #declare starfield_distribu_angle = 4;
   #declare starcluster_excentricity = <1.0, 1.0, 1.0>;
   #declare starcluster_rotation = <0, 0, 0>;
   #if(render_quality) #declare starfield_star_amount = 100; #else #declare starfield_star_amount = 50; #end
   #include "starfield.inc"
   object {O_StarCluster01}

#end

#if (STARFIELD_SCENE_NR = 5)

   #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
   #declare starfield_star_aura = rgb <0.6, 0.75, 1.0>;
   #declare starfield_star_amount = 50; //250
   #declare starfield_starsize_min = 0.1;
   #declare starfield_starsize_max = 1.0;
   #declare starcluster_excentricity = <1, 1, 1>;
   #declare starcluster_rotation = <0, 0, 0>;
   #include "starfield.inc"
   #declare P_Cluster01 = P_StarCluster01;

   #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
   #declare starfield_star_aura = rgb <1.0, 0.75, 0.9>;
   #declare starfield_star_amount = 50; //250
   #declare starfield_starsize_min = 0.1;
   #declare starfield_starsize_max = 0.3;
   #declare starcluster_excentricity = <1, 1, 1>;
   #declare starcluster_rotation = <0, 0, 0>;
   #include "starfield.inc"
   #declare P_Cluster02 = P_StarCluster01;

   #declare SF = 4;
   #declare O_StarField = sky_sphere {
   pigment { average
      pigment_map {
        [SF P_StarField03 rotate starcluster_rotation ]
        [SF P_StarField05 rotate starcluster_rotation ]
        [SF P_Cluster01 scale 0.1 rotate starcluster_rotation ]
        [SF P_Cluster02 scale 0.1 rotate starcluster_rotation ]
        }
      }
   }
   sky_sphere {O_StarField}

#end

// random star cluster
#if (STARFIELD_SCENE_NR = 4)
   
   #declare SeedS = seed(frame_number+1);
   #declare STARFIELDS_NO = IRand(2,4,SeedS);
   #declare P_Cluster = array[STARFIELDS_NO+1];
   
   #declare I=1;   
   #while (I<STARFIELDS_NO)
      #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
      #declare starfield_star_aura = rgb <RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS), RRand(0.6,1.0,SeedS)>;
      #if (I=1) #declare starfield_star_amount = 50; #else #declare starfield_star_amount = IRand(50,100,SeedS); #end
      #declare starfield_starsize_min = RRand(0.1,0.5,SeedS);
      #declare starfield_starsize_max = RRand(1.0,2.0,SeedS);
      #declare starfield_distribu_angle = RRand(1,10,SeedS);
      #declare starcluster_excentricity = <RRand(0.6,2.0,SeedS), 1, 1>;
      #declare starcluster_rotation = <90, 0, RRand(-90,90,SeedS)>;
      #declare starfield_seed_no = 1234567 + frame_number;
      //#declare starfield_skysphere_no = 0;
      #include "starfield.inc"
      //#debug concat("I=",str(I,0,0),"\n")
      #if (I=1) #declare P_Cluster[I] = P_StarCluster03; #else #declare P_Cluster[I] = P_StarCluster01; #end
   #declare I=I+1; #end

   #declare O_StarField = sky_sphere {
   pigment { average
      pigment_map {
         #local I=1; #while (I<STARFIELDS_NO)
            [STARFIELDS_NO+1 P_Cluster[I] scale 0.1 rotate starcluster_rotation ]
         #local I=I+1; #end
         [STARFIELDS_NO+1 stars03 scale 0.1 ]
         }
      }
   }
   sky_sphere {O_StarField}

#end

// star cluster triple mix
#if (STARFIELD_SCENE_NR = 3)

   #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
   #declare starfield_star_aura = rgb <0.6, 0.75, 1.0>;
   #declare starfield_star_amount = 100;
   #declare starfield_starsize_min = 0.1;
   #declare starfield_starsize_max = 2.0;
   #declare starfield_distribu_angle = 5;
   #declare starcluster_excentricity = <1, 1, 1>;
   #declare starcluster_rotation = <90, 0, 0>;
   //#declare starfield_skysphere_no = 8;
   #include "starfield.inc"
   #declare P_Cluster01 = P_StarCluster03;

   #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
   #declare starfield_star_aura = rgb <0.6, 0.75, 1.0>;
   #declare starfield_star_amount = 50; //200
   #declare starfield_starsize_min = 0.5;
   #declare starfield_starsize_max = 1.5;
   //#declare starfield_distribu_angle = 180;
   #declare starcluster_excentricity = <1, 1, 1>;
   #declare starcluster_rotation = <90, 0, 0>;
   //#declare starfield_skysphere_no = 8;
   #include "starfield.inc"
   #declare P_Cluster02 = P_StarCluster01;

   #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
   #declare starfield_star_aura = rgb <1.0, 0.85, 0.8>;
   #declare starfield_star_amount = 50; //200
   #declare starfield_starsize_min = 0.2;
   #declare starfield_starsize_max = 1.0;
   //#declare starfield_distribu_angle = 180;
   #declare starcluster_excentricity = <1, 1, 1>;
   #declare starcluster_rotation = <90, 0, 0>;
   //#declare starfield_skysphere_no = 8;
   #include "starfield.inc"
   #declare P_Cluster03 = P_StarCluster01;

   #declare O_StarField = sky_sphere {
   pigment { average
      pigment_map {
        [3 P_Cluster01 scale 0.1 rotate starcluster_rotation ]
        [3 P_Cluster02 scale 0.1 rotate starcluster_rotation ]
        [3 P_Cluster03 scale 0.1 rotate starcluster_rotation ]
        [1 stars03 scale 0.1 ]
        }
      }
   }
   sky_sphere {O_StarField}

#end

// mix: excentric star cluster and background stars
#if (STARFIELD_SCENE_NR = 2)

   #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
   #declare starfield_star_aura = rgb <1.0, 0.75, 0.6>;
   #declare starfield_star_amount = 20; //70
   #declare starfield_starsize_min = 0.5;
   #declare starfield_starsize_max = 2.0;
   #declare starfield_distribu_angle = 5;
   #declare starcluster_excentricity = <3, 1, 1>;
   #declare starcluster_rotation = <90, 0, -45>;
   //#declare USE_OBJECT_NUMBER=13;
   #include "starfield.inc"
   //#declare P_Cluster01 = P_StarCluster03;
   object { O_StarCluster03 }

   #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
   #declare starfield_star_aura = rgb <0.6, 0.75, 1.0>;
   #declare starfield_star_amount = 50; //255
   #declare starfield_starsize_min = 0.3;
   #declare starfield_starsize_max = 1.5;
   #declare starfield_distribu_angle = 180;
   #declare starcluster_excentricity = <1, 1, 1>;
   #declare starcluster_rotation = <90, 0, 0>;
   #include "starfield.inc"
   //#declare USE_OBJECT_NUMBER=11;
   //#declare P_Cluster02 = P_StarCluster01;
   object { O_StarCluster01 }

/*   #declare O_StarField = sky_sphere {
   pigment { average
      pigment_map {
        //[3 P_Cluster01 scale 0.1 rotate starcluster_rotation ]
        //[3 P_Cluster02 scale 0.1 rotate starcluster_rotation ]
        [1 stars03 scale 0.1 ]
        }
      }
   }
   sky_sphere {O_StarField}
*/
#end

// example of a quick implementation using predefined skyspheres
// globular rotated star cluster
#if (STARFIELD_SCENE_NR = 1)

   #declare starfield_seed_no = 1234567+STARFIELD_NR; // + STARFIELD_NR;
   #declare SeedS = seed(starfield_seed_no);

   #declare starfield_star_color = rgb <0.9, 0.9, 0.9>;
   #declare starfield_star_aura = rgb <0.6, 0.75, 1.0>;
   #declare starfield_starsize_min = 0.5;
   #declare starfield_starsize_max = 2.0;
   #declare starfield_star_amount = 20; //IRand(10,70,SeedS);
   #declare starfield_distribu_angle = RRand(-90,90,SeedS);
   #declare starcluster_excentricity = <RRand(1.0,10.0,SeedS), RRand(1.0,10.0,SeedS), RRand(1.0,10.0,SeedS)>;
   #declare starcluster_rotation = <RRand(0,30,SeedS), RRand(0,30,SeedS), RRand(-90,90,SeedS)>;
   #declare starfield_skysphere_no = frame_number;
   #include "starfield.inc"

#end

//logging
/*   #if (create_logfile)
      #write(LogFile,"O_StarCluster Number = ",I,"\n")
      #write(LogFile,"starfield_star_intensity = ",starfield_star_intensity,"\n")
      #write(LogFile,"starfield_star_color = ",vstr(3,starfield_star_color,", ",0,2),"\n")
      #write(LogFile,"starfield_star_aura = ",vstr(3,starfield_star_aura,", ",0,2),"\n")
      #write(LogFile,"starfield_starsize_min = ",starfield_starsize_min,"\n")
      #write(LogFile,"starfield_starsize_max = ",starfield_starsize_max,"\n")
      #write(LogFile,"starcluster_excentricity = ",vstr(3,starcluster_excentricity,", ",0,2),"\n")
      #write(LogFile,"starcluster_rotation = ",vstr(3,starcluster_rotation,", ",0,1),"\n")
      #write(LogFile,"starfield_star_amount = ",starfield_star_amount,"\n")
   #end
*/
// EOF
