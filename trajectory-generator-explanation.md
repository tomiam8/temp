*Dear the NCSS:*
==============
This was a large project for our robotics team with about three people working on and off on it for about 4 weeks. Also, we still haven’t publicly released all the code yet, and it would have to be in a big archive which you said not to do, so I’ve made this document to describe the project, include some pictures of it, and then also some code snipets (that I specifically wrote). Sorry for uploading non-code in the code section.
Thanks, Tom Schwarz.

Project description
=====================
The FIRST Robotics Competition has teams build and program robots, to compete in 2min 30s games. This year's game involved shooting many small wiffle balls into a goal about 3m off the ground, and delivering yellow plate-sized discs called "gears" across the field. The first 15 seconds of the game is called the autonomous period, where the robot must act independantly from human control. During this period, balls are worth 3x more than normal, and so we decided we needed to drive as quickly and reliably as possible to pick up balls, turn around and go back to the goal to shoot as many balls as possible.

In previous years, we had programmed the robot's movement as a combination of straight lines and curve segments, that we found using guess and check. This wouldn't however be accurate or fast enough for our needs, and so we decided to create a program to drive the robot along a smooth pre-planned curve, and a GUI program to let us plan these curves.

Pictures
=============
* A sample path being made in the GUI
![Sample random path being made in the GUI](https://i.imgur.com/te4DCGw.png)
* The second section of the path used by the robot to shoot
* ![The second section of the path used by the robot to shoot](https://i.imgur.com/DJVNJxb.png)
* Video 1 (horizontal view), Shenzhen regional- https://youtu.be/Ffp9beXsky0
* Video 2 (aerial view), Sydney regional 2 Finals match 1 - the robot is in the bottom left corner of the screen - https://youtu.be/fN21pvv2aFo


Code snippets
==============
Beizer curve generator code - based on https://en.wikipedia.org/wiki/De_Casteljau%27s_algorithm:
```Java
	private static Double[] calculateWaypoints(ArrayList<Double[]>linePoints, int order, double pointNum, int pointsTotal) {
		ArrayList<Double[]> resultPoints = new ArrayList<Double[]>();
		Double x1, y1, x2, y2, xValue, yValue, heading;
		for (int linePointCounter=1; linePointCounter < linePoints.size(); linePointCounter++) {
			x1 = (linePoints.get(linePointCounter-1))[0];
			x2 = (linePoints.get(linePointCounter))[0];
			y1 = (linePoints.get(linePointCounter-1))[1];
			y2 = (linePoints.get(linePointCounter))[1];
			xValue = x1 + (pointNum/pointsTotal)*(x2-x1);
			yValue = y1 + (pointNum/pointsTotal)*(y2-y1);
			
			if (x2-x1==0) {
				if (y2>y1) {
					heading = 0.0;
				}
				else {
					heading = 180.0;
				}
			}
			
			else if (y2-y1==0) {
				if (x2>x1) {
					heading = 90.0; 
				}
				else {
					heading = -90.0;
				}
			}
			
			else {
				heading = (Math.toDegrees(Math.atan((y2-y1)/(x2-x1))) + 90)%360;
				if (heading > 180) {heading -= 360;}
			}
			resultPoints.add(new Double[]{xValue, yValue, heading});
		}
		return (order == 1) ? resultPoints.get(0) : calculateWaypoints(resultPoints, order-1, pointNum, pointsTotal);
	}
```

Line Drawing code:
```Java
	/**
	 * A function which will draw lines between the various points given to it. Made in mind to draw the beizer curve onto the JPanel
	 * @param g Graphics gotten from JPanel to draw onto 
	 * @param resultWayPoints the points to draw from, should be formatted as resultWayPoints
	 */
	private void drawBeizerCurve(Graphics2D g2D, ArrayList<double[]> resultWayPoints) {
		double x1, y1, x2, y2, individualScaleFactorPoint1, individualScaleFactorPoint2;
		double xScale = this.panelWidth/(resultWayPoints.get(resultWayPoints.size()-1)[0]); //Divide the distance between the ends of the curve by the size of the sreen
		double yScale = this.panelHeight/(resultWayPoints.get(resultWayPoints.size()-1)[1]); ///10*9 because the menu bar takes up the top 10th
		double scaleFactor = (xScale < yScale) ? xScale : yScale; //Use smaller scale for both dimensions so image dosen't get distorted
		//scaleFactor -= 10; //Gives slight buffer so it dosen't draw off the edge of the screen or end perfectly on the edge
		for (int waypointCounter = 1; waypointCounter < resultWayPoints.size(); waypointCounter++) {
			individualScaleFactorPoint1 = scaleFactor*((double)(waypointCounter-1)/resultWayPoints.size());
			individualScaleFactorPoint2 = scaleFactor*((double) waypointCounter/resultWayPoints.size());
			x1 = (resultWayPoints.get(waypointCounter-1)[0]);
			y1 = (resultWayPoints.get(waypointCounter-1)[1]);
			x2 = (resultWayPoints.get(waypointCounter)[0]);
			y2 = (resultWayPoints.get(waypointCounter)[1]);
			g2D.draw(new Line2D.Double(x1*individualScaleFactorPoint1, (this.panelHeight-y1)*individualScaleFactorPoint1, x2*individualScaleFactorPoint2, (y2-this.panelHeight)*individualScaleFactorPoint2));
		}
```
