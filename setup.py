from setuptools import setup, find_packages

setup(name='pykinect2b',
      version='0.2.0',
      description='Wrapper to expose Kinect for Windows v2 API in Python rebranded so that pip install works again',
      license='MIT',
      author='Microsoft Corporation (Kinect V2)',
      author_email='k.hoefle@doktoranden.hs-mannheim.de',
      url='https://github.com/Kinect/PyKinect2/',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License'],
      packages=find_packages(),
      install_requires=['numpy>=1.9.2',
                        'comtypes>=1.1.1']
     )
