
#!/usr/bin/env bash
LB='\033[1;34m'
RR='\033[1;31m'
NC='\033[0m' # No Color
bench_tag=${LB}[A-Bench]${NC}

if [[ $# -eq 0 ]] ; then
    ./$0 --help
    exit 0
fi

for var in "$@"
do
case  $var  in

#--------------------------------------------------------------------------------------[ Experiment ]--
(run) #                  -- ProcFedure to run the experiment described by the steps below. 
    echo -e "Experiment TAG: #$ex_tag"
    echo -e "$bench_tag Running defined experiment... "
    
;;
#----------------------------------------------------------------------------[ Experiment-Functions ]--
(build) #              -- Procedure to build your kube infrastructure (docker).  via custom script.
    echo -e "$bench_tag Deploying the infrastructure of the experiment.     | $RR cus_build $NC"
    
    eval $(minikube docker-env)
    docker build -t xhadoop .
;;
(deploy) #      -- Procedure to deploy your benchmark on kubernetes.     via custom script.
    echo -e "$bench_tag Deploying the infrastructure of the experiment.     | $RR cus_deploy $NC"
    cd charts
    nameOfHadoopCluster='xhadoop'
    helm delete     --purge $nameOfHadoopCluster
    helm install    --name  $nameOfHadoopCluster xhadoop


    helm delete --purge sql-mysql
    sleep 30s
    helm install --name sql-mysql \
    --set mysqlRootPassword=a,mysqlUser=hive,mysqlPassword=password,mysqlDatabase=metastore \
    xmysql

    echo -e  "${bench_tag} hadoop cluster started and named as < $nameOfHadoopCluster > ..."
;;
(bd) #              -- Procedure to build your kube infrastructure (docker).  via custom script.
    ./$0 build
    ./$0 deploy
;;
(d) #         -- connects to a node
    kubectl exec -it xhadoop-hadoop-hdfs-nn-0  -- bash -c " bash ";;
(deb) #         -- connects to a node
    kubectl exec -it xhadoop-hadoop-hdfs-nn-0  -- bash -c " hadoop fs -mkdir -p /tmp && \
                                                    hadoop fs -mkdir -p /user/hive/warehouse && \
                                                    hadoop fs -chmod g+w /tmp && \
                                                    hadoop fs -chmod g+w /user/hive/warehouse
                                                    "
    kubectl exec -it xhadoop-hadoop-hdfs-nn-0  -- bash -c "cd .. && mkdir loop && cd loop && \
    schematool -dbType mysql -initSchema -verbose && \
    bash
    "
;;
(test-had) #    -- executes a simple check
    kubectl exec xhadoop-hadoop-hdfs-nn-0 -- hdfs dfsadmin -report
;;

(--help|*) #                -- Prints the help and usage message
    echo -e  "${bench} USAGE $var <case>"
    echo -e 
    echo -e  The following cases are available:
    echo -e 
    # An intelligent means of printing out all cases available and their
 	# section. WARNING: -E is not portable!
    grep -E '^(#--+\[ |\([a-z_\|\*-]+\))' < "$0" | cut -c 2- | \
    sed -E -e 's/--+\[ (.+) \]--/\1/g' -e 's/(.*)\)$/ * \1/g' \
    -e 's/(.*)\) # (.*)/ * \1 \2/g'
;;
esac     
done