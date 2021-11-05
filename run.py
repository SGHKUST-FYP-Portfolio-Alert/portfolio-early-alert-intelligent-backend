import coloredlogs
import uvicorn

coloredlogs.install(level='INFO', fmt='%(asctime)s %(name)s[%(process)d] %(funcName)s %(levelname)s %(message)s')

if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, reload=True)
