export interface job {
  name: string;
  status: string;
  prompt: string;
  uuid: string;
}

const jobListEmpty: job[] = [];

export const useJobQueue = defineStore("useJobQueue", {
  state: () => ({
    joblist: useLocalStorage("joblist", jobListEmpty),
  }),
  actions: {
    set(joblist: job[]) {
      this.joblist = joblist;
    },
    // remove specific job
    remove(job: job) {
      this.joblist.forEach((item, index) => {
        if (item.name === job.name) this.joblist.splice(index, 1);
      });
    },
    // add new & replace if job already exist
    // TODO, might need to find a way to add at old index to avoid item changes to last place
    add(job: job) {
      this.joblist.forEach((item, index) => {
        if (item.name === job.name) this.joblist.splice(index, 1);
      });
      this.joblist.push(job);
    },
  },
});
