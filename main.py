def define_env(env):
  "Hook function"

  @env.macro
  def k8spgjira(bugnumber):
      return '[K8SPG-'+str(bugnumber)+'](https://jira.percona.com/browse/K8SPG-'+str(bugnumber)+')'
  def cloudjira(bugnumber):
      return '[CLOUD-'+str(bugnumber)+'](https://jira.percona.com/browse/CLOUD-'+str(bugnumber)+')'
