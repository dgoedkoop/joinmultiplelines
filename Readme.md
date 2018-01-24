Join multiple lines
===================
By Daan Goedkoop

Introduction
------------

After selecting multiple features of a line layer, this plugin can merge
them into one feature with a continuous line.

The plugin will automatically put the selected lines in a geographically
logical order and direction. If the end points of two lines do not match
exactly, a line segment between both points is added to make the end result
a single, continuous line. The attributes of the new line will be those of
one of the selected features, but one cannot predict which one.

Testing
-------

A test project / layer has been supplied to experiment with and see the
characteristics of the plugin.

Version history
---------------

* 0.1: 26-04-2013
     * Initial version
* 0.2: 29-04-2013
     * Produce valid geometry if begin and end vertices are identical.
* 0.3: 03-02-2014
     * Update for QGis 2.0
     * Operation is now a single undo/redo-step, instead of having a
       separate step for the removal of the superfluous features.
* 0.4: 22-01-2018
     * Update for QGis 3.0
     * Support multi-part lines
