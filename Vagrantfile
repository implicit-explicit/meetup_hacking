Vagrant.configure('2') do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = 'jayunit100/centos7'

  config.ssh.forward_agent = true

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.provider :virtualbox do |vb|
    vb.customize ['modifyvm', :id, '--memory', '512']
    vb.customize ['modifyvm', :id, '--ioapic', 'on']
  end

  config.vm.provision :shell do |external_shell|
    external_shell.path = 'setup.sh'
  end
end
