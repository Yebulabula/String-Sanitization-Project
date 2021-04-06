<img src="icon.png" align="right" />

# String Sanitization README [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome#readme)

## Environment Configuration:
Install python 3.8 
https://www.python.org/downloads/release/python-380/

- pip install numpy
- pip install pandas
- pip install matplotlib
- pip install Pillow

## Modify the content of the file:
python setup.py build_ext  --inplace

## Dataset:
- SYN (synthetic dataset)
- DNA (the genome of Escherichia coli)
- TRU (Trucks)

## Experimental results (Baseline vs CSD-PLUS)

I. SYN

        1. python3 runner.py -w DataSet/SYN/SYN_W.txt -z DataSet/SYN/SYN_2_Z.txt -s DataSet/SYN/pat_2.txt -k 2 -o 0.5 -c 50 -m 1000 -d 10 -t 3 -e 5
        2. python3 runner.py -w DataSet/SYN/SYN_W.txt -z DataSet/SYN/SYN_3_Z.txt -s DataSet/SYN/pat_3.txt -k 3 -o 0.5 -c 50 -m 1000 -d 10 -t 3 -e 5
        3. python3 runner.py -w DataSet/SYN/SYN_W.txt -z DataSet/SYN/SYN_4_Z.txt -s DataSet/SYN/pat_4.txt -k 4 -o 0.5 -c 50 -m 2000 -d 10 -t 3 -e 5
        4. python3 runner.py -w DataSet/SYN/SYN_W.txt -z DataSet/SYN/SYN_5_Z.txt -s DataSet/SYN/pat_5.txt -k 5 -o 0.5 -c 25 -m 3000 -d 10 -t 3 -e 5
        5. python3 runner.py -w DataSet/SYN/SYN_W.txt -z DataSet/SYN/S5_Z.txt  -s DataSet/SYN/S5.txt  -k 3 -o 0.5 -c 50 -m 1000 -d 10 -t 3 -e 5
        6. python3 runner.py -w DataSet/SYN/SYN_W.txt -z DataSet/SYN/S10_Z.txt -s DataSet/SYN/S10.txt -k 3 -o 0.5 -c 50 -m 1000 -d 10 -t 3 -e 5
        7. python3 runner.py -w DataSet/SYN/SYN_W.txt -z DataSet/SYN/S15_Z.txt -s DataSet/SYN/S15.txt -k 3 -o 0.5 -c 50 -m 3000 -d 10 -t 3 -e 5
        8. python3 runner.py -w DataSet/SYN/SYN_W.txt -z DataSet/SYN/S20_Z.txt -s DataSet/SYN/S20.txt -k 3 -o 0.5 -c 50 -m 3000 -d 10 -t 3 -e 5
   
II. TRU


        1. python3 runner.py -w DataSet/TRU/TRU_W.txt -z DataSet/TRU/TRU_3_Z.txt -s DataSet/TRU/pat_3.txt -k 3 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        2. python3 runner.py -w DataSet/TRU/TRU_W.txt -z DataSet/TRU/TRU_4_Z.txt -s DataSet/TRU/pat_4.txt -k 4 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        3. python3 runner.py -w DataSet/TRU/TRU_W.txt -z DataSet/TRU/TRU_5_Z.txt -s DataSet/TRU/pat_5.txt -k 5 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        4. python3 runner.py -w DataSet/TRU/TRU_W.txt -z DataSet/TRU/TRU_6_Z.txt -s DataSet/TRU/pat_6.txt -k 6 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        5. python3 runner.py -w DataSet/TRU/TRU_W.txt -z DataSet/TRU/S20_Z.txt -s DataSet/TRU/S20.txt -k 4 -o 0.5 -c 25 -m 1000 -d 10 -t 5 -e 5
        6. python3 runner.py -w DataSet/TRU/TRU_W.txt -z DataSet/TRU/S40_Z.txt -s DataSet/TRU/S40.txt -k 4 -o 0.5 -c 25 -m 1000 -d 10 -t 5 -e 5
        7. python3 runner.py -w DataSet/TRU/TRU_W.txt -z DataSet/TRU/S60_Z.txt -s DataSet/TRU/S60.txt -k 4 -o 0.5 -c 25 -m 1000 -d 10 -t 5 -e 5
        8. python3 runner.py -w DataSet/TRU/TRU_W.txt -z DataSet/TRU/S80_Z.txt -s DataSet/TRU/S80.txt -k 4 -o 0.5 -c 25 -m 1000 -d 10 -t 5 -e 5

III. DNA

        1. python3 runner.py -w DataSet/DNA/DNA_W.txt -z DataSet/DNA/DNA_2_Z.txt -s DataSet/DNA/pat_2.txt -k 2 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        2. python3 runner.py -w DataSet/DNA/DNA_W.txt -z DataSet/DNA/DNA_3_Z.txt -s DataSet/DNA/pat_3.txt -k 3 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        3. python3 runner.py -w DataSet/DNA/DNA_W.txt -z DataSet/DNA/DNA_4_Z.txt -s DataSet/DNA/pat_4.txt -k 4 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        4. python3 runner.py -w DataSet/DNA/DNA_W.txt -z DataSet/DNA/DNA_5_Z.txt -s DataSet/DNA/pat_5.txt -k 5 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        5. python3 runner.py -w DataSet/DNA/DNA_W.txt -z DataSet/DNA/S20_Z.txt  -s DataSet/DNA/S20.txt -k 4 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        6. python3 runner.py -w DataSet/DNA/DNA_W.txt -z DataSet/DNA/S40_Z.txt -s DataSet/DNA/S40.txt -k 4 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        7. python3 runner.py -w DataSet/DNA/DNA_W.txt -z DataSet/DNA/S60_Z.txt -s DataSet/DNA/S60.txt -k 4 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5
        8. python3 runner.py -w DataSet/DNA/DNA_W.txt -z DataSet/DNA/S80_Zs.txt -s DataSet/DNA/S80.txt -k 4 -o 0.5 -c 50 -m 1000 -d 10 -t 10 -e 5



## References

- Bernardini, G., Chen, H., Conte, A., Grossi, R., Loukides, G., Pisanti, N., ... & Rosone, G. (2019, September). String sanitization: A combinatorial approach. In Joint European Conference on Machine Learning and Knowledge Discovery in Databases (pp. 627-644). Springer, Cham.
- ["How To Write A Great README"](https://thoughtbot.com/blog/how-to-write-a-great-readme) - *Caleb Thompson (thoughtbot)*
- ["Readme Driven Development"](http://tom.preston-werner.com/2010/08/23/readme-driven-development.html) - *Tom Preston-Werner*
- ["Top ten reasons why I won’t use your open source project"](https://changelog.com/posts/top-ten-reasons-why-i-wont-use-your-open-source-project) - *Adam Stacoviak*
- ["What I learned from an old GitHub project that won 3,000 Stars in a Week"](https://www.freecodecamp.org/news/what-i-learned-from-an-old-github-project-that-won-3-000-stars-in-a-week-628349a5ee14/) - *KyuWoo Choi*

## Tools

- [Common Readme](https://github.com/noffle/common-readme#readme) - A common readme style for Node. Includes a guide and a readme generator.
- [Feedmereadmes](https://github.com/lappleapple/feedmereadmes#readme) - README editing and project analysis/feedback.
- [Hall-of-fame](https://github.com/sourcerer-io/hall-of-fame#readme) - Helps show recognition to repo contributors on README. Features new/trending/top contributors. Updates every hour.
- [Make a README](https://www.makeareadme.com/) - A guide to writing READMEs. Includes an editable template with live Markdown rendering.
- [README best practices](https://github.com/jehna/readme-best-practices#readme) - A place to copy-paste your README.md from
- [readme-md-generator](https://github.com/kefranabg/readme-md-generator#readme) - A CLI that generates beautiful README.md files
- [Standard Readme](https://github.com/RichardLitt/standard-readme#readme) - A standard README style specification. Has a generator to help create spec-compliant READMEs, too.
- [Zalando's README Template](https://github.com/zalando/zalando-howto-open-source/blob/master/READMEtemplate.md#readme) - Simple template to help you cover all the basics.
