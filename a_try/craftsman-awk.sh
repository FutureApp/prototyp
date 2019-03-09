# craft 
docker ps -a | awk '{print $1}'

awkarray=($(kubectl get pods --all-namespaces | awk '{ print $2 }'))
for i in "${awkarray[@]}"
do  
    echo "${awkarray[@]}"
    echo "######## $i ###########"
    kubectl --namespace=kube-system exec -it $i /bin/bash;
    sleep 5
done    

#
kubectl run -it collector-abenchx --image=clio --namespace=kube-system --image-pull-policy=Never -- bash \
    python /collector.py --host monitoring-influxdb --dbname k8s
kubectl cp kube-system/collector-abenchxda-6c85d4b9fd-6txv7:/results/exp_00.xlsx .