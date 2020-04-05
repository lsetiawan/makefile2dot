# A Visualizer for Makefiles

## DESCRIPTION

`makefile2dot` produces a Graphviz `dot` graph from a Makefile. To run it,
install `graphviz` and `python`. This version runs on python 3.

```bash
    sudo apt-get install graphviz python
```

## USAGE

````bash
    makefile2dot <Makefile >out.dot
````

or

````bash
    makefile2dot <Makefile | dot -Tpng > out.png
````
    
## Example

This [example Makefile](https://github.com/vak/makefile2dot/blob/master/Makefile) will result in this png-image:
    
![ScreenShot](https://raw.githubusercontent.com/vak/makefile2dot/master/output-examlple.png)
