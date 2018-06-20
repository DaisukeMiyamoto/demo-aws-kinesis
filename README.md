demo-aws-kinesis
---

Benchmark for Amazon Kinesis Data Streams with AWS Elastic Beanstalk

# Usage

## Prepare

Install awscli and eb cli and set up credentials

```
$ pip install awscli
$ pip install awsebcli
$ pip install locustio
```

## set up Elastic Beanstalk

```
$ cd eb-demo
$ eb init       # Choose region, Python version (3.6 preferred), and SSH keypair.
$ eb create     # Set up environment and chose ELB (ALB preferred)
```

## Benchmark with locust


# Result Examples

## locust

```
 Name                                                          # reqs      # fails     Avg     Min     Max  |  Median   req/s
--------------------------------------------------------------------------------------------------------------------------------------------
 GET /ad?user_id=1                                             344452     1(0.00%)      21      10    4066  |      20   78.70
 GET /ad?user_id=2                                            2761355     2(0.00%)      20      11    4091  |      20  639.40
 GET /ad?user_id=3                                            1034590     1(0.00%)      20      11    4069  |      20  238.10
--------------------------------------------------------------------------------------------------------------------------------------------
 Total                                                        4140397     4(0.00%)                                     956.20
 
Percentage of the requests completed within given times
 Total                                                          288812     48     49     50     50     52     54     66     83   2654
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%

--------------------------------------------------------------------------------------------------------------------------------------------
 GET /ad?user_id=1                                                  13     48     49     50     50     50     52     52     52     52
 GET /ad?user_id=2                                                 104     48     49     51     51     52     54     64     82    102
 GET /ad?user_id=3                                                  38     49     49     50     51     53     59     66     66     66
--------------------------------------------------------------------------------------------------------------------------------------------
 Total                                                             155     48     49     50     51     52     54     64     82    102
```


# Check points


