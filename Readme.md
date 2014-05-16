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

I've developed this plugin up to version 0.2 for use during an internship,
where we sometimes wanted to merge many hundreds of short line segments into
one continuous line feature. That version, in combination with QGis 1.8, has
thus been tested quite intensively. This is an adaptation for QGis 2.0.

A test project / layer has been supplied to experiment with and see the
characteristics of the plugin.

This plugin is different from the "Join Lines" plugin that already exists.
That plugin can handle only two lines at once, and needs a common vertex or
intersection. This plugin can handle any number of lines and can handle
situations where lines have a common vertex or not, but with intersecting
lines it will produce an invalid geometry.

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

License
-------

Copyricht (c) Daan Goedkoop, 2013-2014
All rights reserved.

Redistribution and use in source and binary forms, with or
without modification, are permitted provided that the following
conditions are met:

- Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the following
  disclaimer in the documentation and/or other materials
  provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.